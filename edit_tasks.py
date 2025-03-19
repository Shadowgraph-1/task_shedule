import json
import time
import os

def editor_task(filepath):
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f"Проблема: Файл {filepath} не найден, продолжаем без редактирования задач.")
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
            print(f"Проблема: Файл {filepath} не является валидным JSON файлом, продолжаем без редактирования.")
            return None

        # Проверка содержимого
        if not data:
            print("Проблема: Нет задач для редактирования, ничего не делаем.")
            return True  # Успешное выполнение, но задач нет

        # Отображение задач
        print("Текущие задачи:")
        for idx, (task, time_str) in enumerate(data.items(), 1):
            print(f"{idx}. {task} - {time_str}")

        # Выбор задачи
        choice = input("Введите номер задачи для редактирования: ").strip()
        if not choice:
            print("Проблема: Номер задачи не введён, попробуйте снова.")
            return None  # Некритичная проблема, можно повторить

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(data):
                old_task = list(data.keys())[idx]
            else:
                print("Проблема: Неверный номер задачи, попробуйте снова.")
                return None  # Некритичная проблема, можно повторить
        except ValueError:
            print("Проблема: Неверный ввод (ожидается число), попробуйте снова.")
            return None  # Некритичная проблема, можно повторить

        # Ввод нового названия
        new_task = input("Введите новое название задачи (или нажмите Enter, чтобы оставить прежнее): ").strip()
        if not new_task:
            new_task = old_task

        # Ввод нового времени
        while True:
            new_time = input("Введите новое время задачи (например, '2025-10-10 15:30'): ").strip()
            if not new_time:
                print("Проблема: Время не введено, попробуйте снова.")
                continue
            try:
                time.strptime(new_time, "%Y-%m-%d %H:%M")
                break
            except ValueError:
                print("Проблема: Неверный формат времени. Используйте 'ГГГГ-ММ-ДД ЧЧ:ММ', попробуйте снова.")
                continue

        # Обновление данных
        if new_task != old_task:
            del data[old_task]
        data[new_task] = new_time

        # Сохранение изменений
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=True, indent=4)
            print("Задача успешно обновлена.")
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
    result = editor_task("tasks.json")
    if result:
        print("Редактирование задачи завершено.")
    else:
        print("Редактирование задачи не удалось, возвращаемся в главное меню.")