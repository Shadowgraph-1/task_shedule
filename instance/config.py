from secret_gen import secret_key
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shedule_task.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем предупреждения
    SECRET_KEY = f'{secret_key()}'