"""Точка запуска сервиса ведения дневника."""

from datetime import date

from entries import (filter_entries_by_category, find_entry,
                     get_entries_statistics, sort_entries)
from storage import load_categories, load_entries, save_entries
from utils import input_date, input_int, input_str
from validation import can_save_entry, create_entry, delete_entry

ENTRIES_FILE = "data/entries.json"
CATEGORIES_FILE = "data/categories.json"


def show_entries(entries: dict[int, dict]) -> None:
    """Вывести список записей с содержанием."""
    if not entries:
        print("Записей пока нет.")
        return

    for entry in sort_entries(entries):
        private = "да" if entry["is_private"] else "нет"
        print("-" * 60)
        print(f"[{entry['id']}] {entry['title']}")
        print(f"    Автор:      {entry['user_name']}")
        print(f"    Категория:  {entry['category']}")
        print(f"    Дата:       {entry['entry_date']}")
        print(f"    Настроение: {entry['mood_score']}")
        print(f"    Приватная:  {private}")
        print(f"    Содержание: {entry['content']}")
    print("-" * 60)


def show_statistics(entries: dict[int, dict]) -> None:
    """Вывести статистику по записям."""
    stats = get_entries_statistics(entries)
    print(f"Всего записей: {stats['count']}")
    print(f"Средняя оценка настроения: {stats['avg_mood']}")


def main() -> None:
    """Точка запуска приложения."""
    entries = load_entries(ENTRIES_FILE)
    categories = load_categories(CATEGORIES_FILE)
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
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
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
                    print(f"[{entry['id']}] {entry['title']}")
            else:
                print("Записи не найдены.")

        elif choice == "3":
            entry_date = input_date("Дата: ")
            mood_score = input_int("Оценка настроения (1-10): ")
            print(f"Доступные категории: {', '.join(categories)}")
            category = input_str("Категория: ")
            print(can_save_entry(entry_date, mood_score, category, today))

        elif choice == "4":
            title = input_str("Заголовок: ")
            content = input_str("Содержание: ")
            print(f"Доступные категории: {', '.join(categories)}")
            category = input_str("Категория: ")
            entry_date = input_date("Дата: ")
            mood_score = input_int("Оценка настроения (1-10): ")
            user_name = input_str("Имя пользователя: ")
            private_prompt = "Приватная запись (да/нет): "
            private_answer = input(private_prompt).strip().lower()
            is_private = private_answer == "да"

            result = create_entry(
                entries, title, content, category,
                entry_date, mood_score, user_name, is_private, today,
            )
            if result:
                save_entries(ENTRIES_FILE, entries)
                print("Запись успешно создана.")
            else:
                print(can_save_entry(entry_date, mood_score, category, today))

        elif choice == "5":
            entry_id = input_int("ID записи для удаления: ")
            if delete_entry(entries, entry_id):
                save_entries(ENTRIES_FILE, entries)
                print("Запись удалена.")
            else:
                print("Запись не найдена.")

        elif choice == "6":
            print(f"Доступные категории: {', '.join(categories)}")
            category = input_str("Категория: ")
            filtered = filter_entries_by_category(entries, category)
            if filtered:
                for entry in filtered:
                    entry_id = entry["id"]
                    entry_title = entry["title"]
                    entry_date_str = entry["entry_date"]
                    print(f"[{entry_id}] {entry_title} | {entry_date_str}")
            else:
                print("Записей в этой категории нет.")

        elif choice == "7":
            show_statistics(entries)
        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
