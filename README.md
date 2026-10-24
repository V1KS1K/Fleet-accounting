# Fleet-accounting — система учета автопарка и расписания

Система учета автобусного парка и расписания рейсов на Python с веб-интерфейсом на Django.

## 1. Назначение проекта
Fleet-accounting — учебное приложение для управления автопарком и расписанием рейсов.
Проект позволяет хранить сведения об остановках, маршрутах, водителях, автобусах и рейсах, выполнять основные операции с этими объектами и предоставлять доступ к информации через веб-интерфейс Django.
Проект развивается поэтапно: консольная версия приложения дополняется веб-интерфейсом и постепенно переводится на возможности Django.

## 2. Используемые технологии
* Python 3;
* Django 5.2;
* Django Template Language (DTL);
* HTML5;
* CSS3;
* JavaScript;
* Bootstrap 5.3;
* JSON для хранения данных;
* Git;
* pytest;
* flake8.

## 3. Предметная область
В системе используются основные сущности:
* **Автобус (Bus)** — идентификатор, госномер, маршрут, водитель и статус нахождения на линии;
* **Маршрут (Route)** — идентификатор, название и список остановок;
* **Водитель (Driver)** — идентификатор и ФИО водителя;
* **Остановка (Stop)** — идентификатор и название остановки;
* **Расписание (Schedule)** — идентификатор, автобус, маршрут, время отправления и признак отмены рейса.

Для предметной области реализованы собственные Python-классы.
На текущем этапе данные хранятся в JSON-файлах. Django ORM и база данных приложения пока не используются.

## 4. Структура проекта
```text
Fleet-accounting/
├── buses/
│   ├── templates/
│   │   └── buses/
│   │       ├── includes/
│   │       │   └── bus_card.html
│   │       ├── bus_detail.html
│   │       └── bus_list.html
│   ├── urls.py
│   └── views.py
├── schedules/
│   ├── templates/
│   │   └── schedules/
│   │       ├── includes/
│   │       │   └── schedule_status.html
│   │       ├── schedule_detail.html
│   │       └── schedule_list.html
│   ├── urls.py
│   └── views.py
├── homepage/
│   ├── static/
│   │   └── homepage/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── img/
│   │       │   └── logo.png
│   │       └── js/
│   │           └── main.js
│   ├── templates/
│   │   └── homepage/
│   │       ├── index.html
│   │       └── 404.html
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── includes/
│   │   └── navigation.html
│   └── base.html
├── models/
│   ├── __init__.py
│   ├── bus.py
│   ├── driver.py
│   ├── route.py
│   ├── schedule.py
│   └── stop.py
├── data/
│   ├── buses.json
│   ├── drivers.json
│   ├── routes.json
│   ├── schedules.json
│   └── stops.json
├── tests/
│   ├── test_buses.py
│   ├── test_models.py
│   └── test_schedules.py
├── fleet_project/
│   ├── settings.py
│   └── urls.py
├── main.py
├── storage.py
├── utils.py
├── manage.py
└── README.md