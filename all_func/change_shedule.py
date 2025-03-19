import json
import os
from find_tasks import find_tasks_json

def load_json_file(current_file=None):
    """
    Запрос нового файла расписания.
    
    Если введённое имя совпадает с текущим файлом, спрашиваем, продолжать с ним или искать другой.
    Если выбран другой файл, сначала ищется в локальной директории, затем по всей системе.
    
    Returns:
        str: Путь к новому файлу, если он успешно найден и проверен.
        None: Если пользователь решил продолжить с текущим файлом или произошла критическая ошибка.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Текущая директория скрипта
        
        while True:
            new_file = input("Введите название файла в формате filename.json: ").strip()
            if not new_file:
                print("Проблема: Имя файла не введено, попробуйте снова.")
                continue
            if not new_file.lower().endswith('.json'):
                print("Проблема: Файл должен иметь расширение .json, попробуйте снова.")
                continue

            # Если введённый файл совпадает с текущим
            if current_file and os.path.basename(current_file) == new_file:
                choice = input(f"Файл {new_file} уже загружен. Продолжить с ним? (да/нет): ").strip().lower()
                if choice == "да":
                    print(f"Продолжаем работу с файлом {current_file}")
                    return None
                elif choice == "нет":
                    print("Проблема: Введите другое название файла.")
                    continue
                else:
                    print("Проблема: Неверный выбор (введите 'да' или 'нет'), попробуйте снова.")
                    continue

            # Проверяем файл в текущей директории
            local_path = os.path.join(current_dir, new_file)
            if os.path.exists(local_path):
                try:
                    with open(local_path, 'r', encoding='utf-8') as f:
                        json.load(f)  # Проверка валидности JSON
                    create = input("Импортировать файл? (да/нет): ").strip().lower()
                    if create == "да":
                        print(f"Файл {new_file} успешно импортирован из {local_path}!")
                        return local_path
                    elif create == "нет":
                        print("Проблема: Импорт отменён, попробуйте снова.")
                        continue
                    else:
                        print("Проблема: Неверный выбор (введите 'да' или 'нет'), попробуйте снова.")
                        continue
                except json.JSONDecodeError:
                    print(f"Проблема: {new_file} найден, но не является валидным JSON файлом, попробуйте снова.")
                    continue
                except PermissionError:
                    print(f"Критическая проблема: Нет прав доступа к файлу {local_path}. Возврат в главное меню.")
                    return None
                except OSError as e:
                    print(f"Критическая проблема: Ошибка файловой системы при открытии {local_path} ({e}). Возврат в главное меню.")
                    return None
            else:
                print(f"Проблема: Файл {new_file} не найден в текущей директории, ищем по системе.")
                # Поиск по системе с использованием find_tasks_json
                try:
                    found_files = find_tasks_json(new_file)
                    if not found_files:
                        print(f"Проблема: Файл {new_file} не найден ни в текущей директории, ни в системе, попробуйте снова.")
                        continue
                    
                    print("Найдены следующие файлы в системе:")
                    for idx, path in enumerate(found_files, 1):
                        print(f"{idx}. {path}")
                    choice = input("Выберите файл, введя его номер, или 'c' для отмены: ").strip().lower()
                    
                    if choice == 'c':
                        print("Проблема: Отмена выбора, попробуйте ввести имя файла заново.")
                        continue
                    try:
                        chosen_idx = int(choice) - 1
                        if chosen_idx < 0 or chosen_idx >= len(found_files):
                            print("Проблема: Неверный номер файла, попробуйте снова.")
                            continue
                        chosen_path = found_files[chosen_idx]
                        
                        with open(chosen_path, 'r', encoding='utf-8') as f:
                            json.load(f)  # Проверка валидности JSON
                        print(f"Файл {chosen_path} успешно импортирован!")
                        return chosen_path
                    except ValueError:
                        print("Проблема: Введено некорректное значение номера, попробуйте снова.")
                        continue
                    except json.JSONDecodeError:
                        print(f"Проблема: Выбранный файл {chosen_path} не является валидным JSON файлом, попробуйте снова.")
                        continue
                    except PermissionError:
                        print(f"Критическая проблема: Нет прав доступа к файлу {chosen_path}. Возврат в главное меню.")
                        return None
                    except OSError as e:
                        print(f"Критическая проблема: Ошибка файловой системы при открытии {chosen_path} ({e}). Возврат в главное меню.")
                        return None
                except Exception as e:
                    print(f"Критическая проблема: Ошибка при поиске файлов по системе ({e}). Возврат в главное меню.")
                    return None

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка ({e}). Возврат в главное меню.")
        return None