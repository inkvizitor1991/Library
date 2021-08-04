# Парсер книг с сайта [tululu.org](https://tululu.org)

1. Код позволяет скачать огромное количество книг.
2. Для каждой книги скачивается обложка.
3. Вы получаете словарь, который содержит для каждой книги:
* Название
* Имя автора
* Жанр
* Комментарии

### Как установить
Для запуска блога у вас должен быть установлен [Python 3](https://www.python.org).
1. Установите зависимости командой `pip install -r requirements.txt`
2. Запустите код командой `$ python library.py`


### Аргументы

По умолчанию скачается с 10 по 20 страницу.
Указав аргументы: `--start_id` и `--end_id`,можно задать свой диапазон для скачивания.
```
$ python library.py 20 30
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).