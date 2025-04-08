from flask import Flask
from instance.config import Config
from DB_function import db, Users
from route import register_routes
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)

# Отладочный вывод для проверки конфигурации
print("SQLALCHEMY_DATABASE_URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
print("SQLALCHEMY_TRACK_MODIFICATIONS:", app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS'))
print("SECRET_KEY:", app.config.get('SECRET_KEY'))  # Добавляем отладочный вывод

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    print(f"Загрузка пользователя: {user}")
    return user

register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        migrations_dir = os.path.join(app.root_path, 'migrations')
        if not os.path.exists(migrations_dir):
            print("Папка migrations не существует. Пожалуйста, выполните 'flask db init' для инициализации миграций.")
        else:
            db_file = 'shedule_task.db'
            if not os.path.exists(db_file):
                print("База данных не существует, применяем миграции...")
                upgrade()
            else:
                print("База данных уже существует, проверяем миграции...")
                try:
                    upgrade()
                except Exception as e:
                    print(f"Ошибка при применении миграций: {e}")
    app.run(debug=True)