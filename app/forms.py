from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired
from app.models import Group


grade_list = [('Зачет', 'Зачет'), ('Незачет', 'Незачет'), ('3', '3'), ('4', '4'), ('5', '5')]
type_list = [('Зачет', 'Зачет'), ('Экзамен', 'Экзамен')]
ses_list = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')]


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class AddStudent(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Fullname', validators=[DataRequired()])
    grp_name = SelectField('Group', validators=[InputRequired()])
    u_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteStudent(FlaskForm):
    students = SelectField('Students', validators=[InputRequired()])
    submit = SubmitField('Delete')


class DeleteGroup(FlaskForm):
    groups = SelectField('Groups', validators=[InputRequired()])
    submit = SubmitField('Delete')


class AddGroup(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddSubject(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteSubject(FlaskForm):
    subject = SelectField('Subject', validators=[InputRequired()])
    submit = SubmitField('Delete')


class AddTeacher(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    subject = SelectField('Subject', validators=[InputRequired()])
    submit = SubmitField('Add')


class DeleteTeacher(FlaskForm):
    teacher = SelectField('Name', validators=[InputRequired()])
    submit = SubmitField('Delete')


class PutMark(FlaskForm):
    grade = SelectField('Grade', choices=grade_list, validators=[InputRequired()])
    ses_type = SelectField('Type', choices=type_list, validators=[InputRequired()])
    student = SelectField('Student', validators=[InputRequired()])
    num_sem = SelectField('Number', choices=ses_list, validators=[InputRequired()])
    submit = SubmitField('Put')