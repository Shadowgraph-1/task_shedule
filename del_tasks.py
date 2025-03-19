import json
import os

def delete_tasks(filepath):
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f"Проблема: Файл {filepath} не найден, продолжаем без удаления задач.")
            return None  # Некритичная проблема, продолжаем без задач

        # Чтение файла
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except PermissionError:
            print(f"Критическая проблема: Нет прав доступа к файлу {filepath}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при открытии {filepath} ({e}). Возврат в главное меню.")
            return None
        except json.JSONDecodeError:
            print(f"Проблема: Файл {filepath} не является валидным JSON файлом, продолжаем без удаления задач.")
            return None

        # Проверка содержимого
        if not data:
            print("Проблема: Нет задач для удаления, ничего не делаем.")
            return True  # Успешное выполнение, но задач нет

        # Отображение задач и выбор
        print("Текущие задачи:")
        for idx, (task, time) in enumerate(data.items(), 1):
            print(f"{idx}. {task} - {time}")

        choice = input("Введите номер задачи для удаления: ").strip()
        if not choice:
            print("Проблема: Номер задачи не введён, попробуйте снова.")
            return None  # Некритичная проблема, возвращаем None для повторного запроса

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(data):
                del data[list(data.keys())[idx]]
            else:
                print("Проблема: Неверный номер задачи, попробуйте снова.")
                return None  # Некритичная проблема, можно повторить попытку
        except ValueError:
            print("Проблема: Неверный ввод (ожидается число), попробуйте снова.")
            return None  # Некритичная проблема, можно повторить попытку

        # Сохранение изменений
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=True, indent=4)
            print("Задача удалена.")
            return True  # Успешное выполнение
        except PermissionError:
            print(f"Критическая проблема: Нет прав для записи в файл {filepath}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при записи в {filepath} ({e}). Возврат в главное меню.")
            return None
        except Exception as e:
            print(f"Критическая проблема: Ошибка при сохранении изменений ({e}). Возврат в главное меню.")
            return None

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка ({e}). Возврат в главное меню.")
        return None

# Пример вызова функции
if __name__ == "__main__":
    result = delete_tasks("tasks.json")
    if result:
        print("Удаление задачи завершено.")
    else:
        print("Удаление задачи не удалось, возвращаемся в главное меню.")