import json

def delete_tasks(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if data:
            print("Текущие задачи:")
            for idx, (task, time) in enumerate(data.items(), 1):
                print(f"{idx}. {task} - {time}")
            choice = input("Введите номер задачи для удаления: ")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(data):
                    del data[list(data.keys())[idx]]
                    with open(filepath, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=True, indent=4)
                    print("Задача удалена.")
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Неверный ввод.")
        else:
            print("Нет задач для удаления.")
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка: {filepath} не является валидным JSON файлом.")