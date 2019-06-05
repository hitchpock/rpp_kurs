from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin


class Session(db.Model):
    ses_id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(255), db.ForeignKey('subject.name'))
    grade = db.Column(db.String(255))
    data = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    teach_name = db.Column(db.String(255), db.ForeignKey('teacher.name'))
    ses_type = db.Column(db.String(255), db.ForeignKey('type.type_name'))
    u_id = db.Column(db.String(255), db.ForeignKey('student.u_id'))
    sem_id = db.Column(db.Integer)

    def __repr__(self):
        return "<Session {}>".format(self.ses_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(255))
    students = db.relationship('Student', backref='id', cascade='delete,all', uselist=False)
    teachers = db.relationship('Teacher', backref='id', cascade='delete,all', uselist=False)

    def __repr__(self):
        return "<User {}>".format(self.login)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Subject(db.Model):
    sub_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    teachers = db.relationship('Teacher', backref='subject_name', cascade='delete,all')
    sessions = db.relationship('Session', backref='subject_name')

    def __repr__(self):
        return "<Subject {}>".format(self.name)


class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    students = db.relationship('Student', backref='group', cascade='delete,all')

    def __repr__(self):
        return "<Group {}>".format(self.name)


class Type(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(255), index=True, unique=True)
    sessions = db.relationship('Session', backref='type_ses')


class Teacher(db.Model):
    row_id = db.Column(db.Integer, primary_key=True, nullable=False)
    teach_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), index=True, unique=True)
    sub_name = db.Column(db.String(255), db.ForeignKey('subject.name'))
    sessions = db.relationship('Session', backref='teacher')

    def __repr__(self):
        return "<Teacher {}>".format(self.name)


class Student(db.Model):
    row_id = db.Column(db.Integer, primary_key=True, nullable=False)
    std_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), index=True)
    grp_name = db.Column(db.String(255), db.ForeignKey('group.name'))
    u_id = db.Column(db.String(255), index=True, unique=True)
    sessions = db.relationship('Session', backref='student', cascade='delete,all')

    def __repr__(self):
        return "<Student {}>".format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))