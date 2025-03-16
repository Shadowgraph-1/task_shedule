import json
import time

def add_tasky(TASKS, filepath):
    task = input("Введите задачу: ")
    while True:
        timer_str = input("Введите время задачи (например, '2025-10-10 15:30'): ")
        try:
            time.strptime(timer_str, "%Y-%m-%d %H:%M")
            TASKS[task] = timer_str
            print(f"Задача '{task}' добавлена с временем: {timer_str}")
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(TASKS, file, ensure_ascii=True, indent=4)  # Сохраняем с поддержкой русских символов
            break
        except ValueError:
            print("Ошибка: Неверный формат времени. Используйте 'ГГГГ-ММ-ДД ЧЧ:ММ'.")