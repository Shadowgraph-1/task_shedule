import os
import json

def create_new_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Текущая директория скрипта
    
    while True:
        try:
            new_file = input("Введите файл в формате newfile.json: ").lower().strip()
            
            # Проверяем, заканчивается ли имя файла на .json
            if not new_file:
                print("Проблема: Имя файла не введено, попробуйте снова.")
                continue
            if not new_file.endswith(".json"):
                print("Проблема: Неправильный формат файла (должен заканчиваться на .json), попробуйте снова.")
                continue
            
            # Формируем полный путь к файлу
            filepath = os.path.join(current_dir, new_file)
            
            # Проверяем, существует ли файл
            if os.path.exists(filepath):
                print(f"Проблема: Файл {new_file} уже существует, введите другое имя.")
                continue
            
            # Создаем новый файл
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({}, f)  # Создаем пустой JSON-файл
            print(f"Файл {new_file} создан в директории {filepath} успешно!")
            return filepath  # Возвращаем путь к созданному файлу для дальнейшего использования
        
        except PermissionError:
            print(f"Критическая проблема: Нет прав для создания файла в {current_dir}. Возврат в главное меню.")
            return None  # Возвращаемся в главное меню
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы ({e}). Возврат в главное меню.")
            return None  # Возвращаемся в главное меню
        except Exception as e:
            print(f"Проблема: Ошибка при создании файла ({e}), попробуйте снова.")
            continue  # Продолжаем выполнение, запрашивая ввод заново