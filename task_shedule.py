from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# import bcrypt - хэширование (раскомментируйте, если будете использовать)
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shedule_task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Рекомендуется для отключения предупреждений
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор, первичный ключ
    username = db.Column(db.String(12), unique=True, nullable=False)  # Уникальное имя пользователя
    firstname = db.Column(db.String(50), nullable=False)  # Имя, не уникальное
    lastname = db.Column(db.String(50), nullable=False)  # Фамилия, не уникальная
    mail = db.Column(db.String(120), unique=True, nullable=False)  # Email, уникальный
    password = db.Column(db.String(128), nullable=False)  # Хэшированный пароль

    def __repr__(self):
        return '<Users %r>' % self.id
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор заметки
    new_note_add = db.Column(db.Text, nullable=True)  # Текст заметки
    date_time_note = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)  # Дата и время
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Иностранный ключ

    def __repr__(self):
        return '<Note %r>' % self.user_id

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        mail = request.form['mail']
        password = request.form['password']

        new_user = Users(username=username, firstname=firstname, lastname=lastname, mail=mail, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            db.session.rollback()
            return "Ошибка при регистрации. Возможно, имя пользователя или email уже заняты."
    
    # Если метод GET, показываем форму
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            return redirect(url_for('home'))
        else:
            return "Неверное имя пользователя или пароль"
    
    return render_template('login.html')


@app.route('/add-note', methods=['GET', 'POST'])
def add_note():
    return render_template('add_note.html')


# Создание таблиц при запуске
if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
    app.run(debug=True)