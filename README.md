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

| RU NAME | KEY |
| ------ | ------ |
| База данных | DB_ENGINE |
| Имя базы данных | DB_NAME |
| Логин для подключения к базе данных | POSTGRES_USER |
| Пароль для подключения к БД | POSTGRES_PASSWORD |
| Название сервиса (контейнера) | DB_HOST |
| Порт для подключения к БД | DB_PORT |


### Запуск проекта

- Запустите контейнеры
```sh
docker-compose up -d
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
[84.201.169.6](http://84.201.169.6/)
[http://foodgramm.tk/](http://foodgramm.tk/)
```
- Адрес админ панели:
```
[84.201.169.6/admin](http://84.201.169.6/admin)
```

### Автор

## Данила

> Mail - dankol@mail.ru

> GitHub - [GitHub/Dany-ko](https://github.com/Dany-ko)
