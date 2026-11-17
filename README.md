# Сервис ведения дневника

Консольное приложение ПР3 дополнено веб-интерфейсом на Django.
Страницы формируются шаблонами Django (ПР6).
Данные сайта читаются через Django ORM (ПР9).
Админка, slug категорий, GeneratedField и Debug Toolbar — ПР10.
Исходная база ПР7 (`data/diary.sqlite`) сохранена как источник для переноса.
Создание и удаление через веб-формы будут добавлены на следующих практиках.

## Возможности

Веб-интерфейс (ПР6–ПР10):

- главная страница с навигацией;
- просмотр списка категорий и карточки категории;
- просмотр списка записей и карточки записи;
- фильтр, поиск, сортировка и постраничный вывод записей;
- поиск записей по дате (`GET`);
- статистика числа записей по категориям;
- шаблоны Django (`extends`, `include`, `{% url %}`);
- собственные CSS, изображение и JavaScript;
- модели Django и запросы ORM;
- панель Django Admin, slug категории, GeneratedField;
- статус записи (`TextChoices`) и менеджер `EntryQuerySet`.

Консольная версия (ПР3) сохранена:

- создание и удаление записей;
- поиск, фильтрация, статистика;
- работа с пользователями, категориями и датами;
- хранение данных в JSON.


## Используемые технологии

- Python 3;
- Django 5.2 — веб-фреймворк;
- Django ORM и миграции;
- SQLite (`db.sqlite3` для сайта, `data/diary.sqlite` как исходник ПР7);
- Django Template Language;
- HTML, CSS, JavaScript и Bootstrap 5.3;
- pytest;
- flake8.

## Целевая аудитория

Пользователи, которым нужно фиксировать события и размышления
с привязкой к дате, категории и оценке настроения.

## Предметная область

Основными объектами предметной области являются:

- пользователь;
- категория;
- дата;
- дневниковая запись.

Пользователь создаёт записи дневника в выбранной категории на указанную дату.
Запись хранит ссылки на объекты `UserEntity`, `CategoryEntity` и `DateEntity`,
а не только их идентификаторы.
Несколько записей одного дня ссылаются на один и тот же объект `DateEntity`.
Приватная запись является разновидностью дневниковой записи
и скрывает содержание при выводе.

## Основные сущности (entity)

### UserEntity — пользователь

Объект `UserEntity` представляет автора дневниковых записей.

Основные атрибуты:

- `id` — уникальный идентификатор пользователя;
- `name` — имя пользователя;
- `email` — адрес электронной почты.

Основные методы:

- `validate_email()` — проверка корректности email;
- `from_data()` — создание объекта `UserEntity` из набора данных;
- `matches()` — поиск по имени или почте;
- `__str__()` — строковое представление пользователя.

### CategoryEntity — категория

Объект `CategoryEntity` представляет тематику записи.

Основные атрибуты:

- `id` — уникальный идентификатор категории;
- `name` — название категории.

Основные методы:

- `validate_name()` — проверка названия;
- `from_data()` — создание объекта `CategoryEntity` из набора данных;
- `matches()` — поиск по названию;
- `__str__()` — строковое представление категории.

### DateEntity — дата

Объект `DateEntity` представляет календарный день дневника.

Основные атрибуты:

- `id` — уникальный идентификатор даты;
- `value` — календарное значение дня.

Основные методы:

- `validate_not_future()` — проверка, что дата не в будущем;
- `from_data()` — создание объекта `DateEntity` из набора данных;
- `is_future()` — относится ли дата к будущему;
- `matches()` — совпадение с другой датой;
- `to_iso()` — представление в формате ISO;
- `__str__()` — строковое представление даты.

### EntryEntity — дневниковая запись

Объект `EntryEntity` представляет запись дневника, созданную пользователем.

Основные атрибуты:

- `id` — уникальный идентификатор записи;
- `user` — объект `UserEntity`;
- `category` — объект `CategoryEntity`;
- `entry_date` — объект `DateEntity`;
- `title` — заголовок;
- `content` — содержание;
- `mood_score` — оценка настроения;
- `is_private` — признак приватности.

Основные методы:

- `validate_mood()` — проверка оценки настроения;
- `from_data()` — создание записи из данных JSON;
- `can_be_saved()` — проверка возможности сохранения;
- `matches_title()` — поиск по заголовку;
- `belongs_to_category()` — принадлежность категории;
- `belongs_to_date()` — принадлежность дате;
- `visibility` — текстовый признак приватности;
- `__str__()` — строковое представление записи.

Классы `PublicEntryEntity` и `PrivateEntryEntity` наследуют `EntryEntity`
и по-разному показывают содержание записи.

## Взаимодействие объектов

```text
UserEntity ──создаёт──► EntryEntity
CategoryEntity ◄──относится к── EntryEntity
DateEntity ◄──привязана к── EntryEntity
PublicEntryEntity / PrivateEntryEntity ──является──► EntryEntity
```

При загрузке из JSON идентификаторы `user_id`, `category_id` и `date_id`
преобразуются в ссылки на объекты `UserEntity`, `CategoryEntity` и `DateEntity`.
При сохранении выполняется обратное преобразование.

## Хранение данных

JSON (консоль ПР3):

- `data/users.json`;
- `data/categories.json`;
- `data/dates.json`;
- `data/entries.json`.

Исходная SQLite ПР7 (не меняется сайтом):

- файл: `data/diary.sqlite`;
- схема: `sql/schema.sql`;
- инспекция: `python db/inspect_source_db.py`.

База Django ORM (ПР9–ПР10):

- файл: `db.sqlite3`;
- модели: `User`, `Category`, `DiaryDate`, `Entry`;
- связи `ForeignKey` с `on_delete=PROTECT` и `related_name="entries"`;
- у `Category` поле `slug` и метод `get_absolute_url()`;
- у `Entry` поле `status` (`public` / `private` / `archived`) и `is_high_mood`;
- менеджер `Entry.objects` с методами `public()`, `private()`, `archived()`, `for_date()`;
- миграции в приложениях `users`, `categories`, `dates`, `entries`;
- перенос: `python db/import_sqlite_to_orm.py`.

Страницы сайта читают `db.sqlite3` через ORM, без `sqlite3` во view.

## Страницы веб-интерфейса

- `/` — главная страница (`index()`);
- `/categories/` — список категорий (`Category.objects`);
- `/categories/<slug>/` — категория (`get_absolute_url`);
- `/admin/` — панель администратора;
- `/entries/` — список записей с фильтром, поиском, сортировкой и пагинацией;
- `/entries/by-date/` — поиск записей по дате;
- `/entries/statistics/` — статистика (`annotate` / `aggregate`);
- `/entries/<int:entry_id>/` — запись (`select_related`).

Если категория или запись не найдены, шаблон показывает сообщение,
а `render(..., status=404)` возвращает код 404.
Для адресов без маршрута работает `handler404` → `page_not_found()`.
Свою страницу 404 для неизвестного URL видно при `DEBUG = False`.

Ссылки в шаблонах формируются через `{% url %}` и пространства имён
`homepage`, `categories`, `entries`. HTML во view больше не собирается:
используется `render()`, функция `page()` удалена.

## Структура проекта

```text
service_diary/
│
├── README.md
├── requirements.txt
├── manage.py
├── main.py
├── storage.py
├── utils.py
├── validation.py
│
├── diary/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   └── includes/navigation.html
│
├── homepage/
│   ├── templates/homepage/
│   └── static/homepage/
├── users/
├── categories/
│   └── templates/categories/
├── dates/
├── entries/
│   └── templates/entries/
│
├── models/
├── db/
│   ├── database.py
│   ├── import_json.py
│   ├── inspect_source_db.py
│   └── import_sqlite_to_orm.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── data/
└── tests/
```


## Назначение модулей

### `main.py`

Консольная версия приложения (сохранена с ПР3).

### `diary/`

Пакет настроек Django-проекта: `settings.py`, корневой `urls.py`.

### `templates/`

Общие шаблоны сайта: `base.html` и `includes/navigation.html`.

### `homepage/`

Главная страница: `views.index` и шаблон `homepage/index.html`.
Статика: `css/style.css`, `js/main.js`, `img/logo.png`.

### `users/`

Модель `User`: имя и email автора записей. В админке — inline связанных записей.

### `categories/`

Модель `Category` со `slug` и `get_absolute_url()`.
Список и карточка категории читаются через ORM.
Контекстный процессор `site_stats` добавляет счётчики в шаблоны.

### `dates/`

Модель `DiaryDate` с полем `value` типа `DateField`. Админка дат.

### `entries/`

Модель `Entry` со связями на пользователя, категорию и дату.
Поле `status` (`TextChoices`), менеджер `EntryQuerySet`.
Поле `is_high_mood` вычисляется в БД (`GeneratedField`).
Список — фильтр, поиск, сортировка, `Paginator`.
Карточка — `select_related`. Статистика — категории и статусы.
Статус вынесен в `includes/entry_status.html`.
Админка записей: поиск, фильтры, автодополнение, действия.

### `db/`

`import_json.py` — JSON → база ПР7.
`inspect_source_db.py` — структура `data/diary.sqlite`.
`import_sqlite_to_orm.py` — перенос в `db.sqlite3`.

### `sql/`

Схема таблиц и набор SQL-запросов (выборка, `WHERE`, `JOIN`, агрегаты,
`GROUP BY`, `HAVING`).

### `models/users.py`

Содержит класс `UserEntity` и функции работы с коллекцией пользователей.

### `models/categories.py`

Содержит класс `CategoryEntity` и функции работы с коллекцией категорий.

### `models/dates.py`

Содержит класс `DateEntity` и функции работы с коллекцией дат.

### `models/entries.py`

Содержит классы `EntryEntity`, `PublicEntryEntity`, `PrivateEntryEntity`
и функции работы с коллекцией записей.

### `storage.py`

Отвечает за загрузку и сохранение данных.
Выполняет преобразование JSON → объекты Python и обратно.

### `validation.py`

Содержит функцию `can_save_entry()` из ПР1 и связанные проверки.

### `utils.py`

Содержит вспомогательные функции безопасного ввода.

### `tests/`

Содержит автоматизированные тесты проекта.

## Обработка ошибок

- некорректный ввод пользователя (дата, число) обрабатывается в `utils.py`;
- ошибки при чтении JSON-файлов обрабатываются в `storage.py`;
- программа не завершается аварийно при некорректных данных.

## Требования

- Python 3.x;
- Django 5.2;
- SQLite;
- pytest;
- flake8.

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Запуск приложения

Веб-версия (Django):

```bash
python manage.py runserver
```

Открыть в браузере: http://127.0.0.1:8000/

Панель администратора: http://127.0.0.1:8000/admin/

Суперпользователь Django Auth создаётся отдельно от модели `users.User`:

```bash
python manage.py createsuperuser
```

Миграции и перенос данных ПР7 → ORM:

```bash
python manage.py makemigrations
python manage.py migrate
python db/inspect_source_db.py
python db/import_sqlite_to_orm.py
```

Консольная версия:

```bash
python main.py
```

## Тестирование

```bash
pytest -v
```

Тесты проверяют:

- создание и работу объектов `UserEntity`, `CategoryEntity`, `DateEntity` и `EntryEntity`;
- методы классов;
- создание и удаление записей;
- связь записи с пользователем, категорией и датой;
- правила сохранения записи.

## Проверка качества кода

```bash
flake8 .
```

Форматирование:

```bash
black .
isort .
```

Проверка типов:

```bash
mypy .
```

## Git

Исходный код проекта хранится в Git-репозитории.

```bash
git status
```

## Django Template Language

- базовый шаблон `templates/base.html`, блоки `title` и `content`;
- наследование `{% extends "base.html" %}`;
- включаемые шаблоны: навигация, карточка категории, статус записи;
- контекст: `categories`, `entries`, `category`, `entry`;
- циклы `{% for %}` и `{% empty %}`, условия `{% if %}`;
- фильтры `length` и `default`, дата `entry.entry_date.value|date:"d.m.Y"`;
- именованные URL: `{% url 'categories:list' %}`, `{% url 'entries:detail' entry.id %}`.

## Статические файлы

Каталог `homepage/static/homepage/`: собственный CSS, логотип и JavaScript
(текущий год в подвале). Bootstrap 5.3 сохранён для базовой вёрстки.

## Текущее состояние и план развития

Реализовано (ПР9–ПР10):

- модели `User`, `Category`, `DiaryDate`, `Entry`;
- миграции и база `db.sqlite3`;
- перенос данных из `data/diary.sqlite`;
- представления на Django ORM;
- фильтр, поиск, сортировка и пагинация списка записей;
- Django Admin для всех моделей предметной области;
- `slug` категории, `GeneratedField`, контекстный процессор;
- статус записи `TextChoices` и менеджер QuerySet;
- Django Debug Toolbar (при `DEBUG=True`).