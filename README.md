# Проект Foodgram

## Описание

Foodgram - проект содержащий базу данных с кулинарными рецептами.
Позволяет публиковать рецепты, сохранять к себе в избранное чужие рецепты, а также формировать список покупок для выбранных рецептов.

Проект доступен по [адресу](https://hopedforluck.sytes.net/)

## Стек

- Python
- Django
- DRF
- JWT
- Docker
- Gunicorn
- PostgreSQL
- Yandex Cloud
- NGINX

## Настройка проекта

- Клонировать репозиторий

```bash
git clone
```

- Установить и активировать виртуальное окружение

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

```bash
python -m pip install --upgrade pip
```

- Перейти в папку /backend/

```bash
cd backend
```

- Установить зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

- Выполнить миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

- Запустить проект

```bash
python manage.py runserver
```


## В проекте настроен автоматический деплой проекта на сервер через workflow при каждом пуше в ветку main


## Примеры некоторых запросов API

Регистрация пользователя:  
``` POST /api/v1/auth/signup/ ```  
Получение JWT-токена в обмен на username и confirmation code:  
``` POST /api/v1/auth/token/ ```  
Добавление нового рецепта:  
``` POST /api/v1/recipes/ ```  
Удаление рецепта:  
``` DELETE /api/v1/recipes/{id} ```  
Скачать список покупок:  
``` GET /api/v1/recipes/download_shopping_cart/ ```  
Добавить рецепт в избранное:  
``` POST /api/v1/recipes/{id}/favorite/ ```   
Подписаться на пользователя:  
``` POST /api/v1/users/{id}/subscribe/ ```    



## Полный список запросов API находится в документации по адресу http://127.0.0.1:8000/redoc/
____
Для тестирования работы приложения в терминале [Postman][1] можно воспользоваться коллекцией запросов находящейся в папке [postman_collection][2].



## Автор проекта:

##### Чурилов Александр - [https://github.com/HopedForLuck]

[1]: https://www.postman.com/
[2]: /postman-collection/
