import json
import time

def editor_task(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: {filepath} не является валидным JSON файлом.")
        return
    
    if not data:
        print("Нет задач для редактирования.")
        return
    
    print("Текущие задачи:")
    for idx, (task, time_str) in enumerate(data.items(), 1):
        print(f"{idx}. {task} - {time_str}")
    
    choice = input("Введите номер задачи для редактирования: ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(data):
            old_task = list(data.keys())[idx]
        else:
            print("Неверный номер задачи.")
            return
    except ValueError:
        print("Неверный ввод. Введите номер задачи.")
        return
    
    new_task = input("Введите новое название задачи (или нажмите Enter, чтобы оставить прежнее): ")
    if new_task.strip() == "":
        new_task = old_task
    
    while True:
        new_time = input("Введите новое время задачи (например, '2025-10-10 15:30'): ")
        try:
            time.strptime(new_time, "%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("Ошибка: Неверный формат времени. Используйте 'ГГГГ-ММ-ДД ЧЧ:ММ'.")
    
    if new_task != old_task:
        del data[old_task]
        data[new_task] = new_time
    else:
        data[new_task] = new_time
    
    # 8. Сохранение изменений в файл
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=True, indent=4)
    
    print("Задача успешно обновлена.")