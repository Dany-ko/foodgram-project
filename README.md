# Foodgram project

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Площадка для любителей поесть

Учебный проект по созднию backend'а соцсети на просторах интернета.
Основные цели, которые преследовались в этом проекте.

- Проект доступен по IP или доменному имени.👍
- Все сервисы и страницы доступны для пользователей в соответствии с их правами.👍
- Рецепты на всех страницах сортируются по дате публикации (новые — выше).👍
- Работает фильтрация по тегам, в том числе на странице избранного и на странице рецептов одного автора).👍
- Работает пагинатор (в том числе при фильтрации по тегам).👍
- Обрабатывается ошибка 404.👍

### Значения Базы Данных

| RU NAME | KEY | VALUE |
| ------ | ------ | ------ |
| База данных | DB_ENGINE | django.db.backends.postgresql |
| Имя базы данных | DB_NAME | postgres |
| Логин для подключения к базе данных | POSTGRES_USER | postgres |
| Пароль для подключения к БД | POSTGRES_PASSWORD | postgres |
| Название сервиса (контейнера) | DB_HOST | db |
| Порт для подключения к БД | DB_PORT | 5432 |


### Запуск проекта

- Запустите контейнеры
```sh
docker-compose up
``` 
- Запустить миграции
```sh
docker-compose exec web python manage.py migrate --noinput
```
- Создать супер пользователя
```sh
docker-compose exec web python manage.py createsuperuser
```
- Собрать статику в одну папку
```sh
docker-compose exec web python manage.py collectstatic --no-input 
```
- Проект доступен по адресу:
```
[www.foodgramm.tk](http://foodgramm.tk/)
```
- Адрес админ панели:
```
[www.foodgramm.tk/admin](http://foodgramm.tk/admin)
```

### Автор

## Данила

> Mail - dankol@mail.ru

> GitHub - [GitHub/Dany-ko](https://github.com/Dany-ko)
