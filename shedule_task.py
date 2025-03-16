import json
import os
from load_task import load_tasks
from find_tasks import find_tasks_json
from del_tasks import delete_tasks
from edit_tasks import editor_task
from add_task import add_tasky

# Глобальный словарь для хранения задач
TASKS = {}


# Основной цикл планировщика задач
def task_schedule(filepath):
    while True:
        print("\nВыберите действие:")
        print("1. Добавить задачу")
        print("2. Просмотреть существующие задачи")
        print("3. Выход")
        print("4. Показать содержимое файла с расписанием")
        print("5. Удалить задачу из файла")
        print("6. Редактировать задачу в файле")
        user_choice = input(": ")

        if user_choice == "1":
            add_tasky(TASKS, filepath)

        elif user_choice == "2":
            # Просмотр задач (расшифрованные)
            if TASKS:
                print("Существующие задачи (в памяти):")
                for task, timer in TASKS.items():
                    print(f"Задача: {task}, Время: {timer}")
            else:
                print("Нет существующих задач.")

        elif user_choice == "3":
            # Выход
            print("Выход из программы.")
            break

        elif user_choice == "4":
            # Показать содержимое файла (зашифрованное)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    print(f"Содержимое файла {filepath} (зашифрованное):")
                    print(content)
            except FileNotFoundError:
                print(f"Файл {filepath} не найден.")

        elif user_choice == "5":
            # Удаление задачи из файла
            try:
                delete_tasks(filepath)  # Передаём путь к файлу
                TASKS.update(load_tasks(filepath))  # Обновляем TASKS после удаления
                print("Задача удалена, словарь TASKS обновлён.")
            except Exception as e:
                print(f"Ошибка при удалении задачи: {e}")

        elif user_choice == "6":
            # Редактирование задачи в файле
            try:
                editor_task(filepath)  # Вызов функции редактирования
                TASKS.update(load_tasks(filepath))  # Обновляем TASKS после редактирования
                print("Задача отредактирована, словарь TASKS обновлён.")
            except Exception as e:
                print(f"Ошибка при редактировании задачи: {e}")

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    print("Попытка найти файл с задачами в формате Name_file.json")
    update_task = input("Введите название файла (с учётом регистра, например, tasks.json или укажаите сразу название файла\nпосле поиска в директория будет создан фал с вашем именем файла): ").strip()
    if not update_task:
        print("Название файла не может быть пустым. Завершение программы.")
        exit(1)

    TASKS_JSON = update_task
    start = input(f"Искать файл {TASKS_JSON} на дисках? (да/нет): ").lower()

    if start == "да":
        print(f"Начинаю поиск файла {TASKS_JSON} в файловой системе")
        found_files = find_tasks_json(TASKS_JSON)
        if found_files:
            print("Найдены следующие файлы:")
            for idx, path in enumerate(found_files, 1):
                print(f"{idx}. {path}")
            choice = input("Выберите файл (введите номер) или 'c' для создания нового в текущей директории: ").strip().lower()
            if choice == 'c':
                filepath = os.path.join(os.getcwd(), TASKS_JSON)  # Создаём в текущей директории
                print(f"Создаю новый файл: {filepath}")
            else:
                try:
                    filepath = found_files[int(choice) - 1]
                except (ValueError, IndexError):
                    print("Неверный выбор. Создаю новый файл в текущей директории.")
                    filepath = os.path.join(os.getcwd(), TASKS_JSON)
        else:
            print(f"Файл {TASKS_JSON} не найден на дисках. Создаю новый файл в текущей директории.")
            filepath = os.path.join(os.getcwd(), TASKS_JSON)
    else:
        print("Поиск файла пропущен. Использую файл в текущей директории.")
        filepath = os.path.join(os.getcwd(), TASKS_JSON)

    # Проверяем, существует ли файл, если нет — создаём его
    if not os.path.exists(filepath):
        print(f"Файл {filepath} не существует. Создаю новый файл.")
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump({}, file)  # Создаём пустой словарь

    # Загружаем задачи из файла
    TASKS.update(load_tasks(filepath))
    print(f"Работаю с файлом: {filepath}")

    # Запуск планировщика
    task_schedule(filepath)