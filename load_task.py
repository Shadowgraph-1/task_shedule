import json
# Загрузка задач из указанного файла
def load_tasks(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Возвращаем пустой словарь, если файла нет
    except json.JSONDecodeError:
        print(f"Ошибка: {filepath} не является валидным JSON файлом.")
        return {}