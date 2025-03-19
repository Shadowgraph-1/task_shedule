import json
import os

# Загрузка задач из указанного файла
def load_tasks(filepath):
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f"Проблема: Файл {filepath} не найден, возвращаем пустой словарь задач.")
            return {}  # Некритичная проблема, продолжаем с пустым словарем

        # Чтение файла
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                tasks = json.load(file)
            if not isinstance(tasks, dict):
                print(f"Проблема: Данные в файле {filepath} не являются словарем, возвращаем пустой словарь.")
                return {}  # Некритичная проблема, возвращаем пустой словарь
            print(f"Задачи успешно загружены из файла {filepath}.")
            return tasks  # Успешная загрузка
        except PermissionError:
            print(f"Критическая проблема: Нет прав доступа к файлу {filepath}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при открытии {filepath} ({e}). Возврат в главное меню.")
            return None
        except json.JSONDecodeError:
            print(f"Проблема: Файл {filepath} не является валидным JSON файлом, возвращаем пустой словарь.")
            return {}  # Некритичная проблема, продолжаем с пустым словарем

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка при загрузке задач ({e}). Возврат в главное меню.")
        return None