import argparse
import logging
import os
import pathlib
from urllib.parse import unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup


def parse_book_page(soup):
    comments = soup.find_all('div', class_='texts')
    links_genre = soup.find('span', class_='d_book').find_all('a')
    name, autor = soup.find('body').find('h1').text.split('::')
    parsed_book = {
        'name': name,
        'autor': autor.strip(),
        'text_genre': [tag.text for tag in links_genre],
        'text_comments': [tag.find(class_='black').contents for tag in comments],
    }
    return parsed_book


def download_txt(download_url_response, parsed_book, folder_book):
    pathlib.Path(folder_book).mkdir(parents=True, exist_ok=True)
    filename = f'{book}. {parsed_book["name"]}'.rstrip()
    combined_filepath = os.path.join(folder_book, f'{filename}.txt')
    with open(f'{combined_filepath}', 'w') as file:
        file.write(download_url_response.text)


def download_image(basic_url, soup, folder_img):
    pathlib.Path(folder_img).mkdir(parents=True, exist_ok=True)
    relative_image_url = soup.find(class_='bookimage').find('a').find('img')['src']
    basic_image_url = urljoin(basic_url, relative_image_url)
    response = requests.get(basic_image_url)
    response.raise_for_status()
    parse_image_url = urlsplit(relative_image_url)
    quote_filename = os.path.split(parse_image_url.path)[-1]
    filename = unquote(quote_filename)
    combined_filepath = os.path.join(folder_img, f'{filename}')
    with open(f'{combined_filepath}', 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('__start_id', nargs="?", type=int, default=10)
    parser.add_argument('__end_id', nargs="?", type=int, default=20)
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    folder_book = 'books/'
    folder_img = 'image/'
    for book in range(args.__start_id, args.__end_id + 1):
        try:
            book_id = {'id': book}
            download_url = 'https://tululu.org/txt.php'
            basic_url = f'https://tululu.org/b{book}/'
            basic_url_response = requests.get(basic_url)
            check_for_redirect(basic_url_response)
            basic_url_response.raise_for_status()
            download_url_response = requests.get(download_url, params=book_id)
            check_for_redirect(download_url_response)
            download_url_response.raise_for_status()
            soup = BeautifulSoup(basic_url_response.text, 'lxml')
            parsed_book = parse_book_page(soup)
            download_txt(download_url_response, parsed_book, folder_book)
            download_image(basic_url, soup, folder_img)
        except:
            logging.basicConfig(level=logging.DEBUG)
