import json
import os
from load_task import load_tasks
from find_tasks import find_tasks_json
from del_tasks import delete_tasks
from edit_tasks import editor_task
from add_task import add_tasky
from daily_task_timer import show_task_time
from change_shedule import load_json_file
from continue_edit import edit_continue
from update_last_file import update_last_edit
from all_dir_files import find_local_json_files
from add_new_file import create_new_file

# Глобальный словарь для хранения задач
TASKS = {}

# Основной цикл планировщика задач
def task_schedule(filepath):
    while True:
        print("\nВыберите действие:")
        print("1. Показать существующие расписания в директории")
        print("2. Добавить задачу")
        print("3. Добавить новый файл")
        print("4. Просмотреть существующие задачи и оставшееся время")
        print("5. Выход")
        print("6. Показать содержимое файла с расписанием")
        print("7. Удалить задачу из файла")
        print("8. Редактировать задачу в файле")
        print("9. Импортировать/Переключиться на другой файл")
        print("10. Какой котик ты сегодня?")
        
        user_choice = input(": ").strip()

        if user_choice == "1":
            try:
                json_files = find_local_json_files()
                if json_files:
                    print("Существующие расписания:")
                    for idx, file in enumerate(json_files, 1):
                        print(f"{idx}. {file}")
                else:
                    print("В директории нет .json файлов (кроме last_edit.json).")
            except Exception as e:
                print(f"Ошибка при поиске файлов: {e}. Продолжаем работу.")

        elif user_choice == "2":
            try:
                add_tasky(TASKS, filepath)
                update_last_edit(filepath)
                print("Задача успешно добавлена.")
            except Exception as e:
                print(f"Ошибка при добавлении задачи: {e}. Продолжаем работу.")

        elif user_choice == "3":
            try:
                new_filepath = create_new_file()
                if new_filepath:
                    filepath = new_filepath
                    TASKS.clear()
                    TASKS.update(load_tasks(filepath))
                    update_last_edit(filepath)
                    print(f"Переключено на новый файл: {filepath}")
            except Exception as e:
                print(f"Ошибка при создании нового файла: {e}. Продолжаем работу.")

        elif user_choice == "4":
            if TASKS:
                print("Существующие задачи (в памяти):")
                for task, timer in TASKS.items():
                    print(f"Задача: {task}, Время: {timer}")
                try:
                    show_task_time(filepath)
                except Exception as e:
                    print(f"Ошибка при отображении времени задач: {e}. Продолжаем работу.")
            else:
                print("Нет существующих задач.")

        elif user_choice == "5":
            print("Выход из программы.")
            break

        elif user_choice == "6":
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    print(f"Содержимое файла {filepath}:")
                    print(content)
            except FileNotFoundError:
                print(f"Файл {filepath} не найден. Продолжаем работу.")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}. Продолжаем работу.")

        elif user_choice == "7":
            try:
                delete_tasks(filepath)
                TASKS.update(load_tasks(filepath))
                update_last_edit(filepath)
                print("Задача удалена, словарь TASKS обновлён.")
            except Exception as e:
                print(f"Ошибка при удалении задачи: {e}. Продолжаем работу.")

        elif user_choice == "8":
            try:
                editor_task(filepath)
                TASKS.update(load_tasks(filepath))
                update_last_edit(filepath)
                print("Задача отредактирована, словарь TASKS обновлён.")
            except Exception as e:
                print(f"Ошибка при редактировании задачи: {e}. Продолжаем работу.")

        elif user_choice == "9":
            try:
                new_filepath = load_json_file(current_file=os.path.basename(filepath))
                if new_filepath:
                    filepath = new_filepath
                    TASKS.clear()
                    TASKS.update(load_tasks(filepath))
                    update_last_edit(filepath)
                    print(f"Файл {filepath} успешно загружен.")
                else:
                    print("Продолжаем работу с текущим файлом.")
            except Exception as e:
                print(f"Ошибка при импорте файла: {e}. Продолжаем работу.")

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    print("Попытка загрузить последний отредактированный файл...")
    try:
        last_file = edit_continue()
        if last_file:
            filepath = last_file
            print(f"Работаю с последним файлом: {filepath}")
        else:
            update_task = input("Введите название файла (например, tasks.json): ").strip()
            if not update_task:
                print("Критическая ошибка: Название файла не может быть пустым. Завершение программы.")
                exit(1)

            if not update_task.endswith('.json'):
                update_task += '.json'

            current_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(current_dir, update_task)

            if not os.path.exists(filepath):
                start = input(f"Файл {update_task} не найден локально. Искать на дисках? (да/нет): ").lower()
                if start == "да":
                    found_files = find_tasks_json(update_task)
                    if found_files:
                        print("Найдены следующие файлы:")
                        for idx, path in enumerate(found_files, 1):
                            print(f"{idx}. {path}")
                        choice = input("Выберите файл (номер) или 'c' для создания нового: ").strip().lower()
                        if choice == 'c':
                            filepath = os.path.join(current_dir, update_task)
                        else:
                            try:
                                filepath = found_files[int(choice) - 1]
                            except (ValueError, IndexError):
                                print("Неверный выбор. Создаю новый файл.")
                                filepath = os.path.join(current_dir, update_task)
                    else:
                        print(f"Файл {update_task} не найден. Создаю новый.")
                        filepath = os.path.join(current_dir, update_task)
                else:
                    print("Создаю новый файл в текущей директории.")
                    filepath = os.path.join(current_dir, update_task)

            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as file:
                    json.dump({}, file)
                print(f"Создан новый файл: {filepath}")

            update_last_edit(filepath)

        TASKS.update(load_tasks(filepath))
        task_schedule(filepath)

    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}. Завершение программы.")
        exit(1)