import json
import os
from find_tasks import find_tasks_json

# Функция для загрузки последнего отредактированного файла из last_edit.json
def edit_continue():
    try:
        last_edit_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_edit.json")
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Проверяем существование last_edit.json
        if not os.path.exists(last_edit_path):
            print("Проблема: Файл last_edit.json не найден, продолжаем работу без последнего файла.")
            return None  # Некритичная проблема, продолжаем без последнего файла

        # Чтение файла
        try:
            with open(last_edit_path, "r", encoding="utf-8") as f:
                file_timestamps = json.load(f)
        except PermissionError:
            print(f"Критическая проблема: Нет прав доступа к файлу {last_edit_path}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при открытии {last_edit_path} ({e}). Возврат в главное меню.")
            return None
        except json.JSONDecodeError:
            print(f"Проблема: Файл last_edit.json содержит некорректные данные, продолжаем без последнего файла.")
            return None

        # Проверка содержимого
        if not file_timestamps:
            print("Проблема: В last_edit.json нет записей о файлах, продолжаем без последнего файла.")
            return None

        # Находим последний файл
        latest_file = max(file_timestamps, key=file_timestamps.get)
        latest_path = os.path.join(current_dir, latest_file)

        # Проверяем существование файла
        if os.path.exists(latest_path):
            print(f"Последний отредактированный файл найден: {latest_path} (изменён: {file_timestamps[latest_file]})")
            return latest_path
        else:
            print(f"Проблема: Файл {latest_file} не существует, продолжаем без последнего файла.")
            return None

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка ({e}). Возврат в главное меню.")
        return None
