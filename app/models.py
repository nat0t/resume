from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    resumes = db.relationship('Resume', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return self.username


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    personal = db.relationship('Personal', backref='resume', uselist=False, cascade='all, delete-orphan')
    specialization = db.relationship('Specialization', backref='resume', uselist=False, cascade='all, delete-orphan')
    experience = db.relationship('Experience', backref='resume', uselist=False, cascade='all, delete-orphan')
    education = db.relationship('Education', backref='resume', uselist=False, cascade='all, delete-orphan')
    contact = db.relationship('Contact', backref='resume', uselist=False, cascade='all, delete-orphan')

    __tablename__ = 'resumes'

    def __repr__(self):
        return self.name


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    surname = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    gender = db.Column(db.String(10), nullable=False)
    birthdate = db.Column(db.Date())
    location = db.Column(db.String(100))
    citizenship = db.Column(db.String(20))
    about = db.Column(db.String(100))
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='CASCADE'))

    __tablename__ = 'personal'
    __table_args__ = (
        db.CheckConstraint("gender IN ('male', 'female')", name='check_gender_validity'),
    )

    def __repr__(self):
        return f'{self.surname} {self.name}'


class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    readiness = db.Column(db.String(21), default='рассмотрю предложения')
    salary = db.Column(db.Integer)
    slogan = db.Column(db.String(80))
    specialization = db.Column(db.String(27), nullable=False)
    grade = db.Column(db.String(16), nullable=False)
    skills = db.Column(db.String(255), nullable=False)
    languages = db.Column(db.String(50))
    remote_ready = db.Column(db.Boolean, default=False)
    relocation_ready = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='CASCADE'))


    __tablename__ = 'specializations'
    __table_args__ = (
        db.CheckConstraint(
            "readiness in ('not_looking', 'looking', 'consider')",
            name='check_readiness_validity',
        ),
        db.CheckConstraint(
            "specialization in ('development', 'testing', 'analytics', 'design', 'management', 'security', 'ai')",
            name='check_specialization_validity',
        ),
        db.CheckConstraint(
            "grade in ('no', 'intern', 'junior', 'middle', 'senior', 'lead')",
            name='check_grade_validity',
        ),
    )

    def __repr__(self):
        return self.slogan


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    jobs = db.relationship('Job', backref='experience', cascade='all, delete-orphan')
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='CASCADE'))

    __tablename__ = 'experiences'

    def __repr__(self):
        return f'Experience {self.id}'


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(255))
    specialization = db.Column(db.String(27), nullable=False)
    grade = db.Column(db.String(16), nullable=False)
    position = db.Column(db.String(30))
    start = db.Column(db.Date(), nullable=False)
    finish = db.Column(db.Date())
    about = db.Column(db.String(255))
    skills = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id', ondelete='CASCADE'))

    __tablename__ = 'jobs'
    __table_args__ = (
        db.CheckConstraint(
            "specialization in ('development', 'testing', 'analytics', 'design', 'management', 'security', 'ai')",
            name='check_specialization_validity',
        ),
        db.CheckConstraint(
            "grade in ('no', 'intern', 'junior', 'middle', 'senior', 'lead')",
            name='check_grade_validity',
        ),
    )

    def __repr__(self):
        return self.name


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    schools = db.relationship('School', backref='education', cascade='all, delete-orphan')
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='CASCADE'))

    __tablename__ = 'educations'

    def __repr__(self):
        return ' | '.join([school for school in self.schools])


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    start = db.Column(db.Date(), nullable=False)
    finish = db.Column(db.Date(), nullable=False)
    practice = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    education_id = db.Column(db.Integer, db.ForeignKey('educations.id', ondelete='CASCADE'))

    __tablename__ = 'schools'

    def __repr__(self):
        return self.name


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(120), unique=True)
    telegram = db.Column(db.String(30), unique=True)
    sn_profile = db.Column(db.String(120), unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='CASCADE'))

    __tablename__ = 'contacts'

    def __repr__(self):
        return self.phone or self.email or self.telegram or self.sn_profile
