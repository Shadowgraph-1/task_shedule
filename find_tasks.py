import string
import os

def find_tasks_json(filename):
    # 1. Поиск в локальной директории
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_file_path = os.path.join(current_dir, filename)
    if os.path.exists(local_file_path):
        print(f"Файл найден в локальной директории: {local_file_path}")
        return [local_file_path]  # Возвращаем список с одним файлом

    # 2. Если не найден локально, ищем на всех дисках
    print(f"Файл {filename} не найден в локальной директории. Ищу на всех дисках...")
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    found_files = []
    for drive in drives:
        print(f"Ищу {filename} на диске {drive}")
        try:
            for root, dirs, files in os.walk(drive):
                if filename in files:
                    full_path = os.path.join(root, filename)
                    found_files.append(full_path)
        except PermissionError:
            print(f"Нет доступа к {drive}, пропускаю...")
        except Exception as e:
            print(f"Ошибка на диске {drive}: {e}")
    return found_files