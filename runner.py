from flask_script import Manager, Shell

from app import app, db
from app.models import (
    User, Resume, Personal, Specialization, Experience, Job, Education, School, Contact)


manager = Manager(app)

def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Resume=Resume,
        Personal=Personal,
        Specialization=Specialization,
        Experience=Experience,
        Job=Job,
        Education=Education,
        School=School,
        Contact=Contact,
    )

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
