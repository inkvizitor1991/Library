import pathlib

import requests

books = 10
pathlib.Path('books/').mkdir(parents=True, exist_ok=True)

for book in range(1, books + 1):
    url = f"https://tululu.org/txt.php?id={book}"

    response = requests.get(url)
    response.raise_for_status()
    with open(f'books/new_books {book}.txt', 'wb') as file:
        file.write(response.content)
