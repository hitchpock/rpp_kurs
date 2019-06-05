from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, AddStudent, AddGroup, DeleteStudent, \
	DeleteGroup, AddSubject, DeleteSubject, AddTeacher, DeleteTeacher, \
		PutMark
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.models import Group, User, Student, Teacher, Subject, Session


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter(User.login==form.login.data).all()[0]
		if user is None or not user.check_password(form.password.data):
			flash('Invalid login or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		if user.role == 'admin':
			return redirect(url_for('admin_page'))
		elif user.role == 'teacher':
			return redirect(url_for('index'))
		elif user.role == 'student':
			return redirect(url_for('index'))
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
	if not current_user.is_authenticated or current_user.role != 'admin':
		return redirect(url_for('login'))
	db_group_list = Group.query.all()
	group_list = [(i.name, i.name) for i in db_group_list]
	form1 = AddStudent(prefix="form1")
	form1.grp_name.choices = group_list
	if form1.validate_on_submit() and form1.submit.data:
		old_user = User.query.filter(User.login==form1.login.data).first()
		old_student = Student.query.filter(Student.u_id==form1.u_id.data).first()
		if old_user is not None or old_student is not None:
			flash('User already exists')
			return redirect(url_for('add_student'))
		user = User(login=form1.login.data, role='student')
		user.set_password(form1.password.data)
		# db.session.add(user)
		student = Student(name=form1.name.data, std_id=user.id, grp_name=form1.grp_name.data, u_id=form1.u_id.data)
		user.students = student
		db.session.add(user)
		db.session.add(student)
		db.session.commit()
		flash('User is added')
		return redirect(url_for('add_student'))
	db_student_list = Student.query.all()
	student_list = [(i.std_id, i.name + "\t" + i.grp_name) for i in db_student_list]
	form2 = DeleteStudent(prefix="form2")
	form2.students.choices = student_list
	if form2.validate_on_submit() or form2.submit.data:
		student = User.query.filter(User.id==form2.students.data).all()[0]
		db.session.delete(student)
		db.session.commit()
		flash('User is deleted')
		return redirect(url_for('add_student'))
	return render_template('add_student.html', form1=form1, form2=form2)
		

@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	return redirect('login')


@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
	if not current_user.is_authenticated or current_user.role != 'admin':
		return redirect(url_for('login'))
	form1 = AddGroup(prefix="form1")
	if form1.validate_on_submit() and form1.submit.data:
		old_group = Group.query.filter(Group.name==form1.name.data).first()
		if old_group is not None:
			flash('Group already exists')
			return redirect(url_for('add_group'))
		group = Group(name=form1.name.data)
		db.session.add(group)
		db.session.commit()
		flash('Group is added')
		return redirect(url_for('add_group'))
	db_group_list = Group.query.all()
	group_list = [(i.group_id, i.name) for i in db_group_list]
	form2 = DeleteGroup(prefix="form2")
	form2.groups.choices = group_list
	if form2.validate_on_submit() or form2.submit.data:
		group = Group.query.filter(Group.group_id==form2.groups.data).all()[0]
		for st in group.students:
			us = User.query.filter(User.id==st.std_id).first()
			db.session.delete(us)
		db.session.delete(group)
		db.session.commit()
		flash('Group is deleted')
		return redirect(url_for('add_group'))
	return render_template('add_group.html', form1=form1, form2=form2)


@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
	if not current_user.is_authenticated or current_user.role != 'admin':
		return redirect(url_for('login'))
	form1 = AddSubject(prefix="form1")
	if form1.validate_on_submit() and form1.submit.data:
		old_subject = Subject.query.filter(Subject.name==form1.name.data).first()
		if old_subject is not None:
			flash('Subject already exists')
			return redirect(url_for('add_subject'))
		subject = Subject(name=form1.name.data)
		db.session.add(subject)
		db.session.commit()
		flash('Subject is added')
		return redirect(url_for('add_subject'))
	db_subject_list = Subject.query.all()
	subject_list = [(i.sub_id, i.name) for i in db_subject_list]
	form2 = DeleteSubject(prefix="form2")
	form2.subject.choices = subject_list
	if form2.validate_on_submit() or form2.submit.data:
		subject = Subject.query.filter(Subject.sub_id==form2.subject.data).all()[0]
		db.session.delete(subject)
		db.session.commit()
		flash('Subject is deleted')
		return redirect(url_for('add_subject'))
	return render_template('add_subject.html', form1=form1, form2=form2)


@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
	if not current_user.is_authenticated or current_user.role != 'admin':
		return redirect(url_for('login'))
	db_subject_list = Subject.query.all()
	subject_list = [(i.name, i.name) for i in db_subject_list]
	form1 = AddTeacher(prefix="form1")
	form1.subject.choices = subject_list
	if form1.validate_on_submit() or form1.submit.data:
		old_user = User.query.filter(User.login==form1.login.data).first()
		if old_user is not None:
			flash('Teacher already exists')
			return redirect(url_for('add_teacher'))
		user = User(login=form1.login.data, role='teacher')
		user.set_password(form1.password.data)
		teacher = Teacher(name=form1.name.data, sub_name=form1.subject.data)
		user.teachers = teacher
		db.session.add(user)
		db.session.add(teacher)
		db.session.commit()
		flash('Teacher is added')
		return redirect(url_for('add_teacher'))
	db_teacher_list = Teacher.query.all()
	teacher_list = [(i.name, i.sub_name + "\t" + i.name) for i in db_teacher_list]
	form2 = DeleteTeacher(prefix="form2")
	form2.teacher.choices = teacher_list
	if form2.validate_on_submit() or form2.submit.data:
		t = Teacher.query.filter(Teacher.name==form2.teacher.data).first()
		u = User.query.filter(User.id==t.teach_id).first()
		db.session.delete(u)
		db.session.commit()
		flash('Teacher is deleted')
		return redirect(url_for('add_teacher'))
	return render_template('add_teacher.html', form1=form1, form2=form2)


@app.route('/put_mark', methods=['GET', 'POST'])
def put_mark():
	if not current_user.is_authenticated or current_user.role != 'teacher':
		return redirect(url_for('login'))
	db_student_list = Student.query.all()
	student_list = [(i.u_id, i.grp_name + "\t" + i.name) for i in db_student_list]
	form = PutMark()
	form.student.choices = student_list
	if form.validate_on_submit():
		teacher = Teacher.query.filter(Teacher.teach_id==current_user.id).first()
		session = Session(sub_name=teacher.sub_name, grade=form.grade.data, 
			teach_name=teacher.name, ses_type=form.ses_type.data, 
			u_id=form.student.data, sem_id=form.num_sem.data)
		db.session.add(session)
		db.session.commit()
		flash('Makr is added')
		return redirect(url_for('put_mark'))
	return render_template('put_mark.html', form=form)


def session_number(session_list):
	session_dict = {}
	for session in session_list:
		if session.sem_id in session_dict.keys():
			session_dict[session.sem_id].append(session)
		else:
			session_dict[session.sem_id] = [session]
	lst = []
	for k, value in session_dict.items():
		dct = {"number": k, "lst": value}
		lst.append(dct)
	return lst



@app.route('/check_mark', methods=['GET', 'POST'])
def check_mark():
	if not current_user.is_authenticated or current_user.role != 'student':
		return redirect(url_for('login'))
	dct = {}
	student = Student.query.filter(Student.std_id==current_user.id).first()
	lst = Session.query.filter(Session.u_id==student.u_id).all()
	session_lst = session_number(Session.query.filter(Session.u_id==student.u_id).all())
	return render_template('check_mark.html', session_lst=session_lst)