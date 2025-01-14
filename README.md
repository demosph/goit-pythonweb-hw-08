# Тема 8. Домашня робота

**Мета цього домашнього завдання** — створити REST API для зберігання та управління контактами. API повинен бути побудований з використанням інфраструктури FastAPI та повинен використовувати SQLAlchemy для управління базою даних.

### Технічний опис завдання

1. **Контакти**

Для зберігання контактів вашої системи необхідно організувати базу даних, яка буде містити всю необхідну інформацію.

Ця інформація повинна включати:

Ім'я
Прізвище
Електронна адреса
Номер телефону
День народження
Додаткові дані (необов'язково)

2. **API**

API, яке ви розробляєте, повинно підтримувати базові операції з даними. Нижче наведено список дій, які ваш API повинен мати можливість виконувати::

Створити новий контакт
Отримати список всіх контактів
Отримати один контакт за ідентифікатором
Оновити контакт, що існує
Видалити контакт

3. **CRUD API**

На придачу до базового функціоналу CRUD API також повинен мати наступні функції:

Контакти повинні бути доступні для пошуку за іменем, прізвищем чи адресою електронної пошти (Query параметри).
API повинен мати змогу отримати список контактів з днями народження на найближчі 7 днів.

### Налаштування середовища і запуск програми

1. Для ініціалізації віртуального середовища:

`poetry shell`

2. Для запуску бази даних у контейнері Docker:

`docker run --name goit-pythonweb-hw-08 -p 5432:5432 -e POSTGRES_PASSWORD=hs7cBzQF8JZm6M9G -d postgres`

Ми будемо працюватимемо зі стандартною базою даних із назвою postgres, яка доступна на `localhost:5432`

3. Для виконання початкової міграції:

`alembic revision --autogenerate -m 'Init'`

4. Для застосування початкової міграції до бази даних і створення таблиць на основі визначених моделей:

`alembic upgrade head`

5. Для запуску застосунку запустіть файл `main.py`

`python main.py`

6. Для взаємодії з сервером ми можемо надсилати запити за допомогою Swagger за адресою http://127.0.0.1:8000/docs.
