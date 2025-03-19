import json
import os
import datetime

# Функция для обновления last_edit.json с временными метками всех .json файлов
def update_last_edit(filepath):
    try:
        last_edit_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_edit.json")
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Проверяем доступ к текущей директории
        if not os.path.isdir(current_dir):
            print(f"Критическая проблема: Директория {current_dir} недоступна или не существует. Возврат в главное меню.")
            return None

        # Получаем список всех .json файлов в директории, исключая last_edit.json
        try:
            json_files = [f for f in os.listdir(current_dir) if f.endswith('.json') and f != 'last_edit.json']
        except PermissionError:
            print(f"Критическая проблема: Нет прав доступа к директории {current_dir}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при чтении директории {current_dir} ({e}). Возврат в главное меню.")
            return None

        if not json_files:
            print("Проблема: В директории нет .json файлов (кроме last_edit.json), продолжаем с пустым списком.")

        # Создаем или загружаем существующий словарь с временными метками
        file_timestamps = {}
        if os.path.exists(last_edit_path):
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
                print("Проблема: Ошибка в last_edit.json, создаю новый пустой словарь.")
                file_timestamps = {}  # Некритичная проблема, продолжаем с новым словарем

        # Обновляем словарь: добавляем или обновляем временные метки для всех .json файлов
        for json_file in json_files:
            full_path = os.path.join(current_dir, json_file)
            try:
                mtime = os.path.getmtime(full_path)  # Время последнего изменения файла
                timestamp = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                file_timestamps[json_file] = timestamp
            except PermissionError:
                print(f"Проблема: Нет прав доступа к файлу {full_path}, пропускаем его.")
                continue  # Некритичная проблема, пропускаем файл
            except OSError as e:
                print(f"Проблема: Ошибка файловой системы при доступе к {full_path} ({e}), пропускаем его.")
                continue  # Некритичная проблема, пропускаем файл

        # Записываем обновленный словарь в last_edit.json
        try:
            with open(last_edit_path, "w", encoding="utf-8") as f:
                json.dump(file_timestamps, f, ensure_ascii=False)
            print(f"Файл {last_edit_path} успешно обновлён.")
            return True  # Успешное выполнение
        except PermissionError:
            print(f"Критическая проблема: Нет прав для записи в файл {last_edit_path}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при записи в {last_edit_path} ({e}). Возврат в главное меню.")
            return None
        except Exception as e:
            print(f"Критическая проблема: Ошибка при сохранении изменений в {last_edit_path} ({e}). Возврат в главное меню.")
            return None

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка ({e}). Возврат в главное меню.")
        return None