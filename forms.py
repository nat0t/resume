from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, SubmitField, TextAreaField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-field'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-field'})


class ResumeForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()], render_kw={'class': 'form-field'})


class PersonalForm(FlaskForm):
    image = FileField('Ваша фотография', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    gender = StringField('Пол')
    birthdate = DateField('Дата рождения')
    location = StringField('Местоположение')
    citizenship = StringField('Гражданство')
    about = TextAreaField('О себе')
    submit = SubmitField('Сохранить')


class SpecializationForm(FlaskForm):
    readiness = StringField('Готовность к работе')
    salary = IntegerField('Ожидаемое вознаграждение')
    slogan = StringField('Коротко о себе')
    specialization = StringField('Специализация', validators=[DataRequired()])
    grade = StringField('Ваша квалификация', validators=[DataRequired()])
    skills = TextAreaField('Профессиональные навыки', validators=[DataRequired()])
    languages = StringField('Знание языков')
    remote_ready = BooleanField('Готов к удаленной работе')
    relocation_ready = BooleanField('Готов к переезду')


class JobForm(FlaskForm):
    name = StringField('Название компании', validators=[DataRequired()])
    location = StringField('Местоположение компании')
    specialization = StringField('Специализация', validators=[DataRequired()])
    grade = StringField('Квалификация', validators=[DataRequired()])
    position = StringField('Ваша должность в компании')
    start = DateField('Начало работы')
    finish = DateField('Окончание работы')
    about = TextAreaField('Ваши обязанности и достижения')
    skills = TextAreaField('Применяемые вами навыки')


class SchoolForm(FlaskForm):
    name = StringField('Название учебного заведения', validators=[DataRequired()])
    course = StringField('Название пройденного курса', validators=[DataRequired()])
    start = DateField('Начало учебы')
    finish = DateField('Завершение учебы')
    certificate = FileField('Полученный сертификат', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])


class ContactForm(FlaskForm):
    phone = StringField('Мобильный телефон')
    email = StringField('Электронная почта', validators=[Email()])
    telegram = StringField('Telegram')
    sn_profile = StringField('Личный сайт или профиль в соцсетях')
