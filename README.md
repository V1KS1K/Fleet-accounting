# Fleet-accounting — система учета автопарка и расписания

Учебное веб-приложение для управления автобусным парком, маршрутами и расписанием рейсов.

## Технологии
* Python 3.x
* Django 5.2
* SQLite (доступ к данным через Django ORM)
* Bootstrap 5.3

## Запуск проекта
1. Клонируйте репозиторий:
   `git clone <адрес репозитория>`
2. Создайте и активируйте виртуальное окружение:
   `python -m venv venv`
   `venv\Scripts\activate`
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Примените миграции:
   `python manage.py migrate`
5. Перенесите данные из базы ПР7 в базу Django ORM:
   `python db/import_sqlite_to_orm.py`
6. Запустите сервер разработки:
   `python manage.py runserver`
7. Откройте в браузере адрес `http://127.0.0.1:8000/`

## Модели данных (Django ORM)
* `Stop` (`buses/models.py`) — остановки; поле: `name`.
* `Route` (`buses/models.py`) — маршруты; поле: `name`, связь `ManyToManyField` с `Stop`.
* `Driver` (`buses/models.py`) — водители; поле: `name`.
* `Bus` (`buses/models.py`) — автобусы; поля: `plate`, `on_the_way`, внешние ключи `ForeignKey` на `Route` и `Driver`.
* `Schedule` (`schedules/models.py`) — рейсы расписания; поля: `departure_time`, `is_cancelled`, внешние ключи `ForeignKey` на `Bus` и `Route` (`on_delete=models.PROTECT`).

## Реализованные сценарии (ПР9)
* Просмотр списка автобусов, строковый поиск по госномеру и маршруту, фильтрация по статусу;
* Просмотр детальной карточки автобуса и связанных остановок;
* Поиск свободных автобусов на выбранное время (с учётом отменённых рейсов);
* Просмотр расписания активных рейсов с фильтрацией по времени, маршруту и автобусу;
* Сортировка расписания по времени, маршруту или автобусу;
* Постраничный вывод расписания (`Paginator`) с сохранением GET-параметров через `{% querystring %}`;
* Статистика количества активных рейсов по маршрутам (`annotate`, `Count`, `Q`, `aggregate`).

## Структура проекта
* `buses/` — модели (`Stop`, `Route`, `Driver`, `Bus`) и представления автопарка
* `schedules/` — модель `Schedule`, представления расписания и статистики
* `homepage/` — главная страница и статика
* `templates/` — HTML-шаблоны страниц
* `db/` — скрипты инспекции (`inspect_source_db.py`) и переноса данных в ORM (`import_sqlite_to_orm.py`)