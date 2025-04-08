from flask import render_template, url_for, request, redirect, session
from flask_login import login_required, current_user, login_user, logout_user
from DB_function import db, Users, Note

def register_routes(app):
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            required_fields = ['username', 'firstname', 'lastname', 'email', 'password']
            for field in required_fields:
                if field not in request.form:
                    return f"Ошибка: поле '{field}' отсутствует в форме.", 400

            username = request.form['username']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            mail = request.form['email']
            password = request.form['password']
            email_preferences = 'email-preferences' in request.form
            receive_updates = 'receive-updates' in request.form

            existing_user = Users.query.filter_by(username=username).first()
            if existing_user:
                return "Ошибка: имя пользователя уже занято. Выберите другое имя."

            existing_email = Users.query.filter_by(mail=mail).first()
            if existing_email:
                return "Ошибка: email уже занят. Используйте другой email."

            new_user = Users(
                username=username,
                firstname=firstname,
                lastname=lastname,
                mail=mail,
                password=password,
                email_preferences=email_preferences,
                receive_updates=receive_updates
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                return "Ошибка при регистрации. Попробуйте снова."

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            required_fields = ['username', 'password']
            for field in required_fields:
                if field not in request.form:
                    return f"Ошибка: поле '{field}' отсутствует в форме.", 400

            username = request.form['username']
            password = request.form['password']
            user = Users.query.filter_by(username=username).first()
            if user and user.password == password:
                session.clear()  # Очищаем сессию перед входом
                login_user(user)
                print(f"Пользователь {user.username} авторизован. Перенаправление на /user-personal.")
                return redirect(url_for('user_info'))
            else:
                return "Неверное имя пользователя или пароль"
        
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/add-note', methods=['GET', 'POST'])
    @login_required  # Добавляем @login_required
    def add_note():
        if request.method == 'POST':
            required_fields = ['note']
            for field in required_fields:
                if field not in request.form:
                    return f"Ошибка: поле '{field}' отсутствует в форме.", 400

            note_content = request.form['note']
            user_id = current_user.id  # Используем ID текущего пользователя
            new_note = Note(new_note_add=note_content, user_id=user_id)
            try:
                db.session.add(new_note)
                db.session.commit()
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                return "Ошибка при добавлении заметки"
        return render_template('add_note.html')

    @app.route('/users')
    @login_required  # Раскомментируем @login_required
    def users():
        user = current_user
        return render_template('users.html', users=[user])

    @app.route('/user-personal', methods=['GET', 'POST'])
    @login_required  # Раскомментируем @login_required
    def user_info():
        user = current_user
        print(f"Данные пользователя в /user-personal: {user}")
        print(f"Username: {user.username}, Firstname: {user.firstname}, Lastname: {user.lastname}, Email: {user.mail}")
        if request.method == 'POST':
            required_fields = ['firstname', 'lastname', 'email']
            for field in required_fields:
                if field not in request.form:
                    return f"Ошибка: поле '{field}' отсутствует в форме.", 400

            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            user.mail = request.form['email']
            user.email_preferences = 'email-preferences' in request.form
            user.receive_updates = 'receive-updates' in request.form

            try:
                db.session.commit()
                return redirect(url_for('user_info'))
            except:
                db.session.rollback()
                return "Ошибка при обновлении данных пользователя."

        return render_template('user_personal.html', user=user)

    @app.route('/db-panel')
    def db_panel():
        all_users = Users.query.all()
        print("=== Пользователи в базе данных ===")
        for user in all_users:
            print(f"ID: {user.id}, Username: {user.username}, Firstname: {user.firstname}, Lastname: {user.lastname}, Email: {user.mail}")
            print("Заметки:")
            if user.notes:
                for note in user.notes:
                    print(f"  - {note.new_note_add} (Создано: {note.date_time_note})")
            else:
                print('Заметок нет!')
            print("---")
        return render_template('db_panel.html', users=all_users)
    
    @app.route('/delete-note/<int:note_id>', methods=['POST'])

    @login_required
    def delete_note(note_id):
        note = Note.query.get_or_404(note_id)
        # Проверяем, что заметка принадлежит текущему пользователю
        if note.user_id != current_user.id:
            return "Ошибка: у вас нет прав для удаления этой заметки.", 403

        try:
            db.session.delete(note)
            db.session.commit()
            return redirect(url_for('user_info'))
        except:
            db.session.rollback()
            return "Ошибка при удалении заметки."
        
    @app.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])

    @login_required
    def edit_note(note_id):
        note = Note.query.get_or_404(note_id)
        # Проверяем, что заметка принадлежит текущему пользователю
        if note.user_id != current_user.id:
            return "Ошибка: у вас нет прав для редактирования этой заметки.", 403

        if request.method == 'POST':
            required_fields = ['note']
            for field in required_fields:
                if field not in request.form:
                    return f"Ошибка: поле '{field}' отсутствует в форме.", 400

            note_content = request.form['note']
            note.new_note_add = note_content
            try:
                db.session.commit()
                return redirect(url_for('user_info'))
            except:
                db.session.rollback()
                return "Ошибка при редактировании заметки."

        return render_template('edit_note.html', note=note)