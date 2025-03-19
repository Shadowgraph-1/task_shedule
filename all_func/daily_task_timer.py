import json
import datetime
import os

def show_task_time(filepath):
    time_format = "%Y-%m-%d %H:%M"
    try:
        current_time = datetime.datetime.now()
        
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f"Проблема: Файл {filepath} не найден, продолжаем без отображения задач.")
            return None  # Некритичная проблема, можно продолжить без задач

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
            print(f"Проблема: Файл {filepath} не является валидным JSON файлом, продолжаем без отображения задач.")
            return None

        # Проверка содержимого
        if not data:
            print("Проблема: Нет задач в файле, ничего не отображаем.")
            return True  # Успешное выполнение, но задач нет

        # Отображение задач
        print("Текущие задачи:")
        for idx, (task, timer) in enumerate(data.items(), 1):
            try:
                # Преобразование строки времени задачи в объект datetime
                old_stamp = datetime.datetime.strptime(timer, time_format)
                # Вычисление оставшегося времени
                left_time = old_stamp - current_time
                
                if left_time.total_seconds() <= 0:
                    print(f"{idx}. {task} - время истекло")
                else:
                    # Получаем количество дней и оставшиеся секунды
                    total_days = left_time.days
                    remaining_seconds = left_time.seconds
                    hours = remaining_seconds // 3600
                    minutes = (remaining_seconds % 3600) // 60
                    seconds = remaining_seconds % 60

                    if total_days >= 365:
                        years = total_days // 365
                        days = total_days % 365
                        print(f"{idx}. {task} - оставшееся время: {years} лет {days} дней, {hours:02d}:{minutes:02d}:{seconds:02d}")
                    else:
                        print(f"{idx}. {task} - оставшееся время: {total_days} дней, {hours:02d}:{minutes:02d}:{seconds:02d}")
            except ValueError:
                print(f"Проблема: Неверный формат времени для задачи '{task}' ({timer}), пропускаем эту задачу.")
                continue  # Некритичная проблема, пропускаем задачу и продолжаем

        return True  # Успешное выполнение

    except Exception as e:
        print(f"Критическая проблема: Неожиданная ошибка ({e}). Возврат в главное меню.")
        return None

