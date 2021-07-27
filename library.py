import os
import pathlib

import requests
from bs4 import BeautifulSoup


def generate_books(books):
    for book in range(1, books + 1):
        url_book = f"https://tululu.org/txt.php?id={book}"
        url_title = f'https://tululu.org/b{book}/'
        response = requests.get(url_title)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('body').find('h1')
        title_text = title_tag.text

        name, *autor = title_text.split("::")
        filename = f'{book}. {name}'.rstrip()
        download_txt(url_book, filename)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url_book, filename, folder='books/'):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url_book)
    response.raise_for_status()
    combined_filepath = os.path.join(folder, f'{filename}.txt')
    try:
        check_for_redirect(response)

        with open(f'{combined_filepath}', 'wb') as file:
            file.write(response.content)

    except:
        print(requests.HTTPError)


if __name__ == '__main__':
    books = 10
    generate_books(books)
