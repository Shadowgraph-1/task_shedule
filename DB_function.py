from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin  # Убедитесь, что UserMixin импортирован

db = SQLAlchemy()

class Users(db.Model, UserMixin):  # Убедитесь, что UserMixin указан
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email_preferences = db.Column(db.Boolean, default=False)
    receive_updates = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.id
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    new_note_add = db.Column(db.Text, nullable=True)
    date_time_note = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Note %r>' % self.user_id