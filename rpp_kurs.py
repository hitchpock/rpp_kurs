from app import app, db
from app.models import Session, User, Subject, Group, Type, Teacher, Student


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Session': Session, 'User': User,
            'Subject': Subject, 'Group': Group, 'Type': Type,
            'Teacher': Teacher, 'Student': Student}
