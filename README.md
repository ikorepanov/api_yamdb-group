![Sprint 10](https://github.com/ikorepanov/api_final_yatube/assets/108400524/ffa52e22-449c-4f4b-872a-c1abb995dee1)

# API_YAMDB
## Учебный проект на курсе Python-разработчик Яндекс-Практикума (10 српинт)

### Концепция проекта ###
Настоящий проект призван помочь студендам отточить навыки проектирования, создания и отладки API на базе архитектуры REST с использованием Django Rest Framework.

Проект является логическим продолжением изучения материала в рамках 7, 8, 9 и 10 спринтов.

В ходе проекта 
* были изучены теоретические основы разработки проектов API на базе REST;
* отработаны навыки составления разных типов запросов (GET, POST, PUT и т.д.) к различным таблицам (Title, Genre, Review, Comment) базы данных;
* изучены практические приёмы решения различных прикладных задач (валидация, кастомизация модели User и т.д.);
* получены навыки командрой работы в Git.

### Примеры запросов и ответов: ###
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

### Как запустить проект ###
* Клонировать репозиторий и перейти в него в командной строке: 
```bash
git clone https://github.com/Jjonnie/api_yamdb/
```
```bash
cd api_yamdb
```
* Cоздать и активировать виртуальное окружение: 
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
* Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip 
```
```bash
pip install -r requirements.txt 
```
* Выполнить миграции:
```bash
python manage.py migrate 
```
* Запустить проект:
```bash
python manage.py runserver
```
* Запустить скрипт для загрузки тестовых данных:
```bash
python manage.py runscript load_csv_to_db
```

### Авторы: 
### Александр Новиков, @alexander_novikov
### Шульман Евгений, @jonnie.gray
### Илья Корепанов, @ikorepanov
