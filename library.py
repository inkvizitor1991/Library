import os
import pathlib
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def generate_books(books):
    for book in range(1, books + 1):
        url_book = f"https://tululu.org/txt.php?id={book}"
        basic_url = f'https://tululu.org/b{book}/'
        response = requests.get(basic_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('body').find('h1')
        title_text = title_tag.text
        name, *autor = title_text.split("::")
        filename = f'{book}. {name}'.rstrip()
        try:
            check_for_redirect(response)
            #for teg in soup.find_all('div', class_="texts"):
                #text_comments = teg.find(class_="black").get_text()
                #print(text_comments)

            genre= soup.find('span', class_='d_book').find_all('a')
            text_genre=[teg.text for teg in genre]
            print('Заголовок:', name)
            print(text_genre)
        except:
            pass
        #download_txt(url_book, filename)
        #download_image(basic_url, soup)


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
        #with open(f'{combined_filepath}', 'wb') as file:
            #file.write(response.content)
    except:
        pass


def download_image(basic_url, soup, folder='image/'):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    try:
        relative_image_url = soup.find(class_='bookimage').find('a').find('img')['src']
        basic_image_url = urljoin(basic_url, relative_image_url)
        response = requests.get(basic_image_url)
        response.raise_for_status()
        check_for_redirect(response)
        parse_image_url = urlparse(relative_image_url)
        filename = parse_image_url.path.split('/')[-1]
        combined_filepath = os.path.join(folder, f'{filename}')
        #with open(f'{combined_filepath}', 'wb') as file:
            #file.write(response.content)
    except:
        pass


if __name__ == '__main__':
    books = 10
    generate_books(books)
