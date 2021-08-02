import argparse
import os
import pathlib
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def parse_book_page(response):
    try:
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        comments = soup.find_all('div', class_="texts")
        genre = soup.find('span', class_='d_book').find_all('a')
        name, autor = soup.find('body').find('h1').text.split("::")
        parsed_book = {
            'name': name,
            'autor': autor.strip(),
            "text_genre": [teg.text for teg in genre],
            'text_comments': [teg.find(class_="black").contents for teg in comments],
        }
        return parsed_book
    except:
        pass


def download_txt(download_url, parsed_book, folder_book):
    pathlib.Path(folder_book).mkdir(parents=True, exist_ok=True)
    response = requests.get(download_url)
    response.raise_for_status()
    try:
        filename = f'{book}. {parsed_book["name"]}'.rstrip()
        combined_filepath = os.path.join(folder_book, f'{filename}.txt')
        check_for_redirect(response)
        with open(f'{combined_filepath}', 'wb') as file:
            file.write(response.content)
    except:
        pass


def download_image(basic_url, response, folder_img):
    pathlib.Path(folder_img).mkdir(parents=True, exist_ok=True)

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        relative_image_url = soup.find(class_='bookimage').find('a').find('img')['src']
        basic_image_url = urljoin(basic_url, relative_image_url)
        response = requests.get(basic_image_url)
        response.raise_for_status()
        check_for_redirect(response)
        parse_image_url = urlparse(relative_image_url)
        filename = parse_image_url.path.split('/')[-1]
        combined_filepath = os.path.join(folder_img, f'{filename}')
        with open(f'{combined_filepath}', 'wb') as file:
            file.write(response.content)
    except:
        pass


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('__start_id',nargs="?", type=int, default=10)
    parser.add_argument('__end_id',nargs="?", type=int, default=20)
    return parser


if __name__ == '__main__':
    parser = get_args()
    args = parser.parse_args()
    folder_book = 'books/'
    folder_img = 'image/'
    for book in range(args.__start_id, args.__end_id):
        download_url = f"https://tululu.org/txt.php?id={book}"
        basic_url = f'https://tululu.org/b{book}/'
        response = requests.get(basic_url)
        response.raise_for_status()
        parsed_book = parse_book_page(response)
        download_txt(download_url, parsed_book, folder_book)
        download_image(basic_url, response, folder_img)
