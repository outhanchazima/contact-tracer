from datetime import datetime
from flaskweb import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # one to many realtionship with contacts_log
    contact_person = db.relationship('Contact_log', backref='name', lazy=True)


    def __repr__(self):
        return f"user('{self.username}', '{self.email}', '{self.image_file}')"

class Contact_log(db.Model):
    __tablename__ = 'contact_log'

    contact_id = db.Column(db.Integer, primary_key=True)
    contact_date = db.Column(db.DateTime, nullable=True)

    # relationship with users
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"contact_log('{self.contact_id}'. '{self.user_id}', '{self.contact_date}')"

class Disease(db.Model):
    __tablename__ = 'disease'

    disease_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disease_name: str = db.Column(db.String, nullable=False)
    disease_description:str = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"disease('{self.disease_name}', {self.disease_description})"

class user_disease(db.Model):
    __tablename__ = 'user_disease'

    user_disease_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    disease_id: int = db.Column(db.Integer, db.ForeignKey('disease.disease_id'), nullable=False)
    start_date: datetime = db.Column(db.DateTime, nullable=False)
    end_date: datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"user_disease('{self.disease_id}', '{self.start_date}', '{self.end_date}', '{self.user_id}') "