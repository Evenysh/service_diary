"""Точка запуска сервиса ведения дневника."""

from datetime import date

from models import CategoryEntity, DateEntity, EntryEntity, UserEntity
from models.categories import (
    add_category,
    find_category,
    get_category_names,
    show_categories,
)
from models.dates import add_date, find_date, show_dates
from models.entries import (
    create_entry,
    delete_entry,
    filter_entries_by_category,
    filter_entries_by_date,
    find_entry,
    get_entries_statistics,
    show_entries,
)
from models.users import add_user, find_user, find_user_by_id, show_users
from storage import (
    load_categories,
    load_dates,
    load_entries,
    load_users,
    save_categories,
    save_dates,
    save_entries,
    save_users,
)
from utils import input_date, input_int, input_str
from validation import can_save_entry

USERS_FILE = "data/users.json"
CATEGORIES_FILE = "data/categories.json"
DATES_FILE = "data/dates.json"
ENTRIES_FILE = "data/entries.json"


def show_statistics(entries: list[EntryEntity]) -> None:
    """Вывести статистику по записям."""
    stats = get_entries_statistics(entries)
    print(f"Всего записей: {stats['count']}")
    print(f"Средняя оценка настроения: {stats['avg_mood']}")


def create_new_user(users: list[UserEntity]) -> None:
    """Создать нового пользователя по данным из консоли."""
    name = input_str("Имя пользователя: ")
    email = input_str("Email: ")
    user = add_user(users, name, email)
    if user is None:
        print("Не удалось создать пользователя: проверьте email.")
        return
    save_users(USERS_FILE, users)
    print(f"Пользователь создан: {user}")


def create_new_category(categories: list[CategoryEntity]) -> None:
    """Создать новую категорию по данным из консоли."""
    name = input_str("Название категории: ")
    category = add_category(categories, name)
    if category is None:
        print("Не удалось создать категорию: имя пустое или уже занято.")
        return
    save_categories(CATEGORIES_FILE, categories)
    print(f"Категория создана: {category}")


def create_new_entry(
    entries: list[EntryEntity],
    users: list[UserEntity],
    categories: list[CategoryEntity],
    dates: list[DateEntity],
    today: date,
) -> None:
    """Создать дневниковую запись, связав её с entity-объектами."""
    if not users:
        print("Сначала добавьте пользователя.")
        return
    if not categories:
        print("Сначала добавьте категорию.")
        return

    show_users(users)
    user_id = input_int("ID пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return

    show_categories(categories)
    category_name = input_str("Название категории: ")
    category = find_category(categories, category_name)
    if category is None:
        print("Категория не найдена.")
        return

    title = input_str("Заголовок: ")
    content = input_str("Содержание: ")
    date_value = input_date("Дата (ДД.ММ.ГГГГ): ")
    mood_score = input_int("Оценка настроения (1-10): ")
    private_answer = input("Приватная запись (да/нет): ").strip().lower()
    is_private = private_answer == "да"
    valid_names = get_category_names(categories)
    entry_date = add_date(dates, date_value)

    result = create_entry(
        entries,
        user,
        category,
        title,
        content,
        entry_date,
        mood_score,
        is_private,
        today,
        valid_names,
    )
    if result:
        save_dates(DATES_FILE, dates)
        save_entries(ENTRIES_FILE, entries)
        print(f"Запись успешно создана: {result.id}")
        return

    print(
        can_save_entry(
            date_value,
            mood_score,
            category.name,
            today,
            valid_names,
        )
    )


def check_save_possibility(categories: list[CategoryEntity], today: date) -> None:
    """Проверить возможность сохранения записи без создания объекта."""
    entry_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    mood_score = input_int("Оценка настроения (1-10): ")
    show_categories(categories)
    category = input_str("Категория: ")
    valid_names = get_category_names(categories)
    print(can_save_entry(entry_date, mood_score, category, today, valid_names))


def show_entries_for_date(entries: list[EntryEntity], dates: list[DateEntity]) -> None:
    """Показать записи, связанные с выбранной датой."""
    show_dates(dates)
    date_value = input_date("Дата (ДД.ММ.ГГГГ): ")
    entry_date = find_date(dates, date_value)
    if entry_date is None:
        print("Дата не найдена.")
        return
    filtered = filter_entries_by_date(entries, entry_date)
    if filtered:
        for entry in filtered:
            print(entry)
    else:
        print("Записей на эту дату нет.")


def main() -> None:
    """Точка запуска приложения."""
    users = load_users(USERS_FILE)
    categories = load_categories(CATEGORIES_FILE)
    dates = load_dates(DATES_FILE)
    entries = load_entries(ENTRIES_FILE, users, categories, dates)
    today = date.today()

    while True:
        print("\n=== Сервис ведения дневника ===")
        print("1. Показать записи")
        print("2. Найти запись по заголовку")
        print("3. Проверить возможность сохранения")
        print("4. Создать запись")
        print("5. Удалить запись")
        print("6. Показать записи по категории")
        print("7. Показать статистику настроения")
        print("8. Показать пользователей")
        print("9. Добавить пользователя")
        print("10. Найти пользователя")
        print("11. Показать категории")
        print("12. Добавить категорию")
        print("13. Показать даты")
        print("14. Показать записи по дате")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            save_users(USERS_FILE, users)
            save_categories(CATEGORIES_FILE, categories)
            save_dates(DATES_FILE, dates)
            save_entries(ENTRIES_FILE, entries)
            print("Данные сохранены. До свидания!")
            break

        if choice == "1":
            show_entries(entries)

        elif choice == "2":
            query = input_str("Подстрока в заголовке: ")
            found = find_entry(entries, query)
            if found:
                for entry in found:
                    print(entry)
            else:
                print("Записи не найдены.")

        elif choice == "3":
            check_save_possibility(categories, today)

        elif choice == "4":
            create_new_entry(entries, users, categories, dates, today)

        elif choice == "5":
            entry_id = input_int("ID записи для удаления: ")
            if delete_entry(entries, entry_id):
                save_entries(ENTRIES_FILE, entries)
                print("Запись удалена.")
            else:
                print("Запись не найдена.")

        elif choice == "6":
            show_categories(categories)
            category_name = input_str("Категория: ")
            category = find_category(categories, category_name)
            if category is None:
                print("Категория не найдена.")
                continue
            filtered = filter_entries_by_category(entries, category)
            if filtered:
                for entry in filtered:
                    print(entry)
            else:
                print("Записей в этой категории нет.")

        elif choice == "7":
            show_statistics(entries)

        elif choice == "8":
            show_users(users)

        elif choice == "9":
            create_new_user(users)

        elif choice == "10":
            query = input_str("Имя или email: ")
            found = find_user(users, query)
            if found:
                for user in found:
                    print(user)
            else:
                print("Пользователи не найдены.")

        elif choice == "11":
            show_categories(categories)

        elif choice == "12":
            create_new_category(categories)

        elif choice == "13":
            show_dates(dates)

        elif choice == "14":
            show_entries_for_date(entries, dates)

        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
