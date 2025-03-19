import json
import time

def add_tasky(TASKS, filepath):
    try:
        task = input("Введите задачу: ").strip()
        if not task:
            print("Проблема: Задача не введена, попробуйте снова.")
            return None  # Возвращаемся в главное меню, так как задача обязательна

        while True:
            timer_str = input("Введите время задачи (например, '2025-10-10 15:30'): ").strip()
            if not timer_str:
                print("Проблема: Время не введено, попробуйте снова.")
                continue

            try:
                time.strptime(timer_str, "%Y-%m-%d %H:%M")  # Проверка формата времени
                TASKS[task] = timer_str
                break  # Выходим из цикла, если формат верный
            except ValueError:
                print("Проблема: Неверный формат времени. Используйте 'ГГГГ-ММ-ДД ЧЧ:ММ', попробуйте снова.")
                continue

        # Сохранение задачи в файл
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(TASKS, file, ensure_ascii=True, indent=4)  # Сохраняем с отступами
            print(f"Задача '{task}' добавлена с временем: {timer_str}")
            return True  # Успешное завершение, возвращаем True
        except PermissionError:
            print(f"Критическая проблема: Нет прав для записи в файл {filepath}. Возврат в главное меню.")
            return None
        except OSError as e:
            print(f"Критическая проблема: Ошибка файловой системы при записи в {filepath} ({e}). Возврат в главное меню.")
            return None
        except Exception as e:
            print(f"Проблема: Ошибка при сохранении задачи в файл ({e}), задача не сохранена.")
            return None  # Возвращаемся в меню, так как сохранение не удалось

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка ({e}). Возврат в главное меню.")
        return None