import os
from datetime import datetime
from urllib.parse import urlsplit

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from forms import PersonalForm, LoginForm, ResumeForm, SpecializationForm, ContactForm, JobForm, SchoolForm

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Development/resume/database.db'

manager = Manager(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))


UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))

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
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))


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
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))

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
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'))

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
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))

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
    education_id = db.Column(db.Integer, db.ForeignKey('educations.id'))

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
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))

    __tablename__ = 'contacts'

    def __repr__(self):
        return self.phone or self.email or self.telegram or self.sn_profile


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    print(f'? {current_user.is_authenticated}')
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()

        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.username)
                # Перенаправление на страницу "next"
                next_page = request.args.get('next')
                print(next_page, urlsplit(next_page).netloc)
                if not next_page or urlsplit(next_page).netloc != '':
                    next_page = url_for('index')

                return redirect(next_page)
            else:
                flash('Неверный пароль. Попробуйте снова.', 'alert-danger')
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user, remember=form.username)

            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ResumeForm()

    if form.validate_on_submit():
        db.session.add(Resume(name=form.name.data, user_id=current_user.get_id()))
        db.session.commit()

    resumes = db.session.query(Resume).filter_by(user_id=current_user.get_id()).all()

    return render_template('index.html', resumes=resumes, form=form)


# @app.route('/resume/<int:resume_id>/')
# @login_required
# def resume(resume_id):
#     return redirect(url_for('personal', resume_id=resume_id))


@app.route('/edit_resume/<int:resume_id>/', methods=['GET', 'POST'])
@login_required
def edit_resume(resume_id):
    personal = db.session.query(Personal).filter_by(resume_id=resume_id).first()

    if not personal:
        return redirect(url_for('create_personal', resume_id=resume_id))

    return redirect(url_for('edit_personal', resume_id=resume_id))


@app.route('/delete_resume/<int:resume_id>/', methods=['GET', 'POST'])
@login_required
def delete_resume(resume_id):
    db.session.query(Resume).filter_by(user_id=current_user.get_id(), id=resume_id).delete()
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/resumes/<int:resume_id>/create_personal/', methods=['GET', 'POST'])
@login_required
def create_personal(resume_id):
    form = PersonalForm()

    if form.validate_on_submit():
        data = {field: value for field, value in form.data.items() if field not in ('csrf_token', 'submit')}
        personal = Personal(resume_id=resume_id, **data)

        file = request.files['image']

        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            personal.image = filename

        db.session.add(personal)
        db.session.commit()

        return redirect(url_for('edit_personal', resume_id=resume_id))

    return render_template('personal.html', resume_id=resume_id, form=form)


@app.route('/resumes/<int:resume_id>/edit_personal/', methods=['GET', 'POST'])
@login_required
def edit_personal(resume_id):
    personal = db.session.query(Personal).filter_by(resume_id=resume_id).first()
    form = PersonalForm(request.form, obj=personal)

    if form.validate_on_submit():
        filename = personal.image
        form.populate_obj(personal)
        file = request.files['image']

        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        personal.image = filename

        db.session.commit()

        return redirect(url_for('edit_personal', resume_id=resume_id))

    return render_template(
        'personal.html',
        resume_id=resume_id,
        active_page='personal',
        image=personal.image if personal else None,
        form=form,
    )



# @app.route('/specialization/')
# @login_required
# def specialization():
#     return render_template('specialization.html', active_page='specialization')

@app.route('/resumes/<int:resume_id>/create_specialization/', methods=['GET', 'POST'])
@login_required
def create_specialization(resume_id):
    form = SpecializationForm()

    if form.validate_on_submit():
        data = {field: value for field, value in form.data.items() if field not in ('csrf_token', 'submit')}
        specialization = Specialization(resume_id=resume_id, **data)
        db.session.add(specialization)
        db.session.commit()

        return redirect(url_for('edit_specialization', resume_id=resume_id))

    return render_template('specialization.html', resume_id=resume_id, form=form)


@app.route('/resumes/<int:resume_id>/edit_specialization/', methods=['GET', 'POST'])
@login_required
def edit_specialization(resume_id):
    specialization = db.session.query(Specialization).filter_by(resume_id=resume_id).first()

    if not specialization:
        return redirect(url_for('create_specialization', resume_id=resume_id))

    form = SpecializationForm()
    # Заполнение формы значениями из БД
    form.skills.data = specialization.skills
    for field_name, value in specialization.__dict__.items():
        if field_name in form.data:
            field = getattr(form, field_name)

            if field.render_kw:
                field.render_kw['value'] = value
            else:
                field.render_kw = {'value': value}

    if form.validate_on_submit():
        form.populate_obj(specialization)
        db.session.commit()

        return redirect(url_for('edit_specialization', resume_id=resume_id))

    return render_template(
        'specialization.html',
        resume_id=resume_id,
        active_page='specialization',
        form=form,
    )


# @app.route('/experience/')
# @login_required
# def experience():
#     return render_template('experience.html', active_page='experience')

@app.route('/resumes/<int:resume_id>/create_experience/', methods=['GET', 'POST'])
@login_required
def create_experience(resume_id):
    experience = Experience(resume_id=resume_id)
    db.session.add(experience)
    db.session.commit()

    return redirect(url_for('edit_experience', resume_id=resume_id))


@app.route('/resumes/<int:resume_id>/edit_experience/', methods=['GET', 'POST'])
@login_required
def edit_experience(resume_id):
    experience = db.session.query(Experience).filter_by(resume_id=resume_id).first()

    if not experience:
        return redirect(url_for('create_experience', resume_id=resume_id))

    return render_template(
        'experience.html',
        resume_id=resume_id,
        experience_id=experience.id,
        jobs=[{'id': job.id, 'name': job.name} for job in experience.jobs],
        active_page='experience',
    )


@app.route('/resumes/<int:resume_id>/edit_experience/<int:experience_id>/create_job/', methods=['GET', 'POST'])
@login_required
def create_job(resume_id, experience_id):
    return redirect(url_for('edit_job', resume_id=resume_id, experience_id=experience_id, job_id=0))


@app.route('/resumes/<int:resume_id>/edit_experience/<int:experience_id>/edit_job/<int:job_id>/', methods=['GET', 'POST'])
@login_required
def edit_job(resume_id, experience_id, job_id):
    form = JobForm()

    if job_id != 0:
        job = db.session.query(Job).filter_by(id=job_id).first()

        # Заполнение формы значениями из БД
        form.about.data = job.about
        form.skills.data = job.skills
        for field_name, value in job.__dict__.items():
            if field_name in form.data:
                field = getattr(form, field_name)

                if field.render_kw:
                    field.render_kw['value'] = value
                else:
                    field.render_kw = {'value': value}
    else:
        job = Job(experience_id=experience_id)

    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.add(job)
        db.session.commit()

        return redirect(url_for('edit_experience', resume_id=resume_id))

    return render_template(
        'job.html',
        resume_id=resume_id,
        experience_id=experience_id,
        job_id=job.id,
        active_page='experience',
        form=form,
    )


@app.route('/resumes/<int:resume_id>/edit_experience/<int:experience_id>/delete_job/<int:job_id>/', methods=['GET', 'POST'])
@login_required
def delete_job(resume_id, experience_id, job_id):
    db.session.query(Job).filter_by(id=job_id).delete()
    db.session.commit()

    return redirect(url_for('edit_experience', resume_id=resume_id))


# @app.route('/education/')
# @login_required
# def education():
#     return render_template('education.html', active_page='education')

@app.route('/resumes/<int:resume_id>/create_education/', methods=['GET', 'POST'])
@login_required
def create_education(resume_id):
    education = Education(resume_id=resume_id)
    db.session.add(education)
    db.session.commit()

    return redirect(url_for('edit_education', resume_id=resume_id))


@app.route('/resumes/<int:resume_id>/edit_education/', methods=['GET', 'POST'])
@login_required
def edit_education(resume_id):
    education = db.session.query(Education).filter_by(resume_id=resume_id).first()

    if not education:
        return redirect(url_for('create_education', resume_id=resume_id))

    return render_template(
        'education.html',
        resume_id=resume_id,
        education_id=education.id,
        schools=[{'id': school.id, 'name': school.name} for school in education.schools],
        active_page='education',
    )


@app.route('/resumes/<int:resume_id>/edit_education/<int:education_id>/create_school/', methods=['GET', 'POST'])
@login_required
def create_school(resume_id, education_id):
    return redirect(url_for('edit_school', resume_id=resume_id, education_id=education_id, school_id=0))


@app.route('/resumes/<int:resume_id>/edit_education/<int:education_id>/edit_school/<int:school_id>/', methods=['GET', 'POST'])
@login_required
def edit_school(resume_id, education_id, school_id):
    form = SchoolForm()

    if school_id != 0:
        school = db.session.query(School).filter_by(id=school_id).first()

        # Заполнение формы значениями из БД
        for field_name, value in school.__dict__.items():
            if field_name in form.data:
                field = getattr(form, field_name)

                if field.render_kw:
                    field.render_kw['value'] = value
                else:
                    field.render_kw = {'value': value}
    else:
        school = School(education_id=education_id)

    if form.validate_on_submit():
        form.populate_obj(school)
        db.session.add(school)
        db.session.commit()

        return redirect(url_for('edit_education', resume_id=resume_id))

    return render_template(
        'school.html',
        resume_id=resume_id,
        education_id=education_id,
        school_id=school.id,
        active_page='education',
        form=form,
    )


@app.route('/resumes/<int:resume_id>/edit_experience/<int:education_id>/delete_job/<int:school_id>/', methods=['GET', 'POST'])
@login_required
def delete_school(resume_id, education_id, school_id):
    db.session.query(School).filter_by(id=school_id).delete()
    db.session.commit()

    return redirect(url_for('edit_education', resume_id=resume_id))


# @app.route('/contact/')
# @login_required
# def contact():
#     return render_template('contact.html', active_page='contact')

@app.route('/resumes/<int:resume_id>/create_contact/', methods=['GET', 'POST'])
@login_required
def create_contact(resume_id):
    form = ContactForm()

    if form.validate_on_submit():
        data = {field: value for field, value in form.data.items() if field not in ('csrf_token', 'submit')}
        contact = Specialization(resume_id=resume_id, **data)
        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('edit_contact', resume_id=resume_id))

    return render_template('contact.html', resume_id=resume_id, form=form)


@app.route('/resumes/<int:resume_id>/edit_contact/', methods=['GET', 'POST'])
@login_required
def edit_contact(resume_id):
    contact = db.session.query(Specialization).filter_by(resume_id=resume_id).first()

    if not contact:
        return redirect(url_for('create_contact', resume_id=resume_id))

    form = ContactForm()
    # Заполнение формы значениями из БД
    for field_name, value in contact.__dict__.items():
        if field_name in form.data:
            field = getattr(form, field_name)

            if field.render_kw:
                field.render_kw['value'] = value
            else:
                field.render_kw = {'value': value}

    if form.validate_on_submit():
        form.populate_obj(contact)
        db.session.commit()

        return redirect(url_for('edit_contact', resume_id=resume_id))

    return render_template(
        'contact.html',
        resume_id=resume_id,
        active_page='contact',
        form=form,
    )


if __name__ == '__main__':
    manager.run()
