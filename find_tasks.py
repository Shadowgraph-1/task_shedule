import string
import os

def find_tasks_json(filename):
    try:
        if not filename:
            print("Проблема: Имя файла не указано, продолжаем без поиска.")
            return []  # Некритичная проблема, возвращаем пустой список

        # 1. Поиск в локальной директории
        current_dir = os.path.dirname(os.path.abspath(__file__))
        local_file_path = os.path.join(current_dir, filename)

        # Проверяем доступ к текущей директории
        if not os.path.isdir(current_dir):
            print(f"Критическая проблема: Директория {current_dir} недоступна или не существует. Возврат в главное меню.")
            return None

        if os.path.exists(local_file_path):
            try:
                # Проверяем, что файл доступен для чтения
                with open(local_file_path, 'r', encoding='utf-8') as f:
                    pass  # Просто проверяем открытие
                print(f"Файл найден в локальной директории: {local_file_path}")
                return [local_file_path]  # Возвращаем список с одним файлом
            except PermissionError:
                print(f"Критическая проблема: Нет прав доступа к файлу {local_file_path}. Возврат в главное меню.")
                return None
            except OSError as e:
                print(f"Критическая проблема: Ошибка файловой системы при доступе к {local_file_path} ({e}). Возврат в главное меню.")
                return None

        # 2. Если не найден локально, ищем на всех дисках
        print(f"Проблема: Файл {filename} не найден в локальной директории. Ищу на всех дисках...")
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        if not drives:
            print("Проблема: Нет доступных дисков для поиска, продолжаем без результатов.")
            return []  # Некритичная проблема, возвращаем пустой список

        found_files = []
        for drive in drives:
            print(f"Ищу {filename} на диске {drive}")
            try:
                for root, dirs, files in os.walk(drive):
                    if filename in files:
                        full_path = os.path.join(root, filename)
                        try:
                            # Проверяем, что файл доступен для чтения
                            with open(full_path, 'r', encoding='utf-8') as f:
                                pass  # Просто проверяем открытие
                            found_files.append(full_path)
                        except PermissionError:
                            print(f"Проблема: Нет прав доступа к файлу {full_path}, пропускаем.")
                            continue  # Некритичная проблема, пропускаем файл
                        except OSError as e:
                            print(f"Проблема: Ошибка файловой системы при доступе к {full_path} ({e}), пропускаем.")
                            continue  # Некритичная проблема, пропускаем файл
            except PermissionError:
                print(f"Проблема: Нет доступа к диску {drive}, пропускаю...")
                continue  # Некритичная проблема, пропускаем диск
            except Exception as e:
                print(f"Проблема: Ошибка на диске {drive} ({e}), пропускаю...")
                continue  # Некритичная проблема, пропускаем диск

        if not found_files:
            print(f"Проблема: Файл {filename} не найден ни на одном диске, продолжаем без результатов.")
        else:
            print(f"Найдено файлов: {len(found_files)}")
        return found_files  # Возвращаем список найденных файлов

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка при поиске файла ({e}). Возврат в главное меню.")
        return None

# Пример вызова функции
if __name__ == "__main__":
    result = find_tasks_json("tasks.json")
    if result is not None:
        print(f"Результат поиска: {result}")
    else:
        print("Поиск файла не удался, возвращаемся в главное меню.")