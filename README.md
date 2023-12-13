![Sprint 10](https://github.com/ikorepanov/api_final_yatube/assets/108400524/ffa52e22-449c-4f4b-872a-c1abb995dee1)
# Проект YaMDb
## Описание проекта
Учебный *групповой* проект в рамках 10 спринта курса Python-разработчик Яндекс Практикума.  

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся.  

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен.  

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).  

Добавлять произведения, категории и жанры может только администратор.  

Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Содержание
1. [Структура проекта](#структура-проекта)
2. [Как запустить проект](#как-запустить-проект)
3. [Стек технологий](#стек-технологий)
4. [Авторы, контакты](#авторы-контакты)

## Структура проекта
Документация API доступна по адресу `http://127.0.0.1:8000/redoc/`.

Задание - написать бэкенд проекта (приложение **reviews**) и **API** для него (приложение **api**) так, чтобы они полностью соответствовали документации.

### Ресурсы API YaMDb
- Ресурс **auth**: аутентификация.
- Ресурс **users**: пользователи.
- Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песня).
- Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.  

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.  

### Пользовательские роли и права доступа
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песням), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.  

### Самостоятельная регистрация новых пользователей
1. Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. Сервис **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).  

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.  

После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором
Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая есть в документации). При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения.  

После этого пользователь должен самостоятельно отправить свой `email` и `username` на эндпоинт `/api/v1/auth/signup/` , в ответ ему должно прийти письмо с кодом подтверждения.  

Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.  

### Связанные данные и каскадное удаление
При удалении объекта пользователя **User** должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).  

При удалении объекта произведения **Title** должны удаляться все отзывы к этому произведению и комментарии к ним.  

При удалении объекта отзыва **Review** должны быть удалены все комментарии к этому отзыву.  

При удалении объекта категории **Category** не нужно удалять связанные с этой категорией произведения.  

При удалении объекта жанра **Genre** не нужно удалять связанные с этим жанром произведения.  

### База данных
По заданию, в директории */api_yamdb/static/data*, подготовлены несколько файлов в формате csv с контентом для ресурсов Users, Titles, Categories, Genres, Reviews и Comments.  

Для автоматической загрузки тестовых данных из csv-файлов - написан кастомный загрузчик.

### Распределение задач в команде
- **Первый разработчик - Александр Новиков**  
[![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=social&logo=Telegram)](https://t.me/alexnewvikov)

  Пишет всю часть, касающуюся управления пользователями:
  - систему регистрации и аутентификации,
  - права доступа,
  - работу с токеном,
  - систему подтверждения через e-mail.   

- **Второй разработчик - Евгений Шульман**  
[![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=social&logo=Telegram)](https://t.me/jonniegray)

  Пишет модели, view и эндпойнты для
  - произведений,
  - категорий,
  - жанров.

- **Третий разработчик - Илья Корепанов**  
[![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=social&logo=Telegram)](https://t.me/number_one_lobster)

  Работает над
  - отзывами,
  - комментариями,
  - рейтингом произведений,
  - реализует импорт данных из csv файлов.

### Примеры запросов
### GET: /api/v1/titles/{title_id}/reviews/ ###
*200:* 
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### POST: /api/v1/titles/{title_id}/reviews/ ###
*400:* 
```JSON
{
  "field_name": [
    "string"
  ]
}
```
### POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/ ###
*201:*
```JSON
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

## Как запустить проект
В дальнейших командах используйте `python3` вместо `python` - **для Linux и macOS**.   
- клонируйте репозиторий:
  ```
  git clone git@github.com:ikorepanov/api_yamdb-group.git
  ```
- перейдите в папку с проектом:
  ```
  cd api_yamdb-group
  ```
- разверните виртуальное окружение:
  ```
  python -m venv venv
  ```
- активируйте виртуальное окружение:
  * команда для Windows
    ```
    source venv/Scripts/activate
    ```
  * команда для Linux и macOS
    ```
    source venv/bin/activate
    ```
- обновите `pip`:
  ```
  python -m pip install --upgrade pip
  ```
- установите зависимости:
  ```
  pip install -r requirements.txt
  ```
- перейдите в папку `api_yamdb`:
  ```
  cd api_yamdb
  ```
- выполните миграции:
  ```
  python manage.py migrate
  ```
- запустите скрипт для загрузки тестовых данных:
  ```
  python manage.py runscript load_csv_to_db
  ```
- создайте суперпользователя:
  ```
  python manage.py createsuperuser
  ```
- запустите сервер разработчика:
  ```
  python manage.py runserver
  ```

Проект будет доступен по адресу [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/).  
Админка проекта: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).  
Для доступа - использовать данные суперпользователя, созданные ранее.  
Отправку запросов на эндпоинты удобно осуществлять через [Postman](https://www.postman.com/).  
Документация доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/).  

## Стек технологий
- Python 3.9
- Django 2.2.9
- Django Rest Framework

## Авторы, контакты
- Илья Корепанов  
[![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=social&logo=Telegram)](https://t.me/number_one_lobster) [![Gmail Badge](https://img.shields.io/badge/Gmail-red?style=social&logo=Gmail)](mailto:ikorepanov.study@gmail.com)  
- Александр Новиков  
[![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=social&logo=Telegram)](https://t.me/alexnewvikov)  
- Евгений Шульман  
[![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=social&logo=Telegram)](https://t.me/jonniegray)  
- Yandex Practicum
