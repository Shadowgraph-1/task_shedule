import os
import json

# Функция для поиска всех .json файлов в локальной директории
def find_local_json_files():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Текущая директория скрипта
        
        # Проверяем доступ к директории
        if not os.path.isdir(current_dir):
            print(f"Критическая проблема: Директория {current_dir} недоступна или не существует. Возврат в главное меню.")
            return None
        
        # Получаем список файлов
        try:
            files = os.listdir(current_dir)
        except PermissionError:
            print(f"Критическая проблема: Нет прав доступа к директории {current_dir}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при чтении директории {current_dir} ({e}). Возврат в главное меню.")
            return None
        
        # Фильтруем только .json файлы, исключая last_edit.json
        json_files = [f for f in files if f.endswith('.json') and f != 'last_edit.json']
        
        if not json_files:
            print("Проблема: В директории нет .json файлов (кроме last_edit.json). Продолжаем работу.")
        
        return json_files  # Возвращаем список найденных файлов

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка при поиске файлов ({e}). Возврат в главное меню.")
        return None