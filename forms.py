from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, DateField, SubmitField, TextAreaField, IntegerField, BooleanField, PasswordField)
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-field login-field'})
    password = PasswordField(
        'Пароль', validators=[DataRequired()], render_kw={'class': 'form-field login-field'})
    submit = SubmitField('Войти или зарегистрироваться', render_kw={'class': 'submit-button'})


class ResumeForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()], render_kw={'class': 'form-field'})
    submit = SubmitField('Создать', render_kw={'class': 'submit-button'})


class PersonalForm(FlaskForm):
    image = FileField('Ваша фотография', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    gender = SelectField('Пол', choices=[('male', 'мужской'), ('female', 'женский')], default='male')
    birthdate = DateField('Дата рождения')
    location = StringField('Местоположение')
    citizenship = StringField('Гражданство')
    about = TextAreaField('О себе')
    submit = SubmitField('Сохранить', render_kw={'class': 'submit-button'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self:
            if field.name in ('submit', 'csrf_token'):
                continue

            if hasattr(field, 'render_kw') and field.render_kw:
                existing_classes = field.render_kw.get('class', '')
                field.render_kw['class'] = (existing_classes + ' form-field').strip()
            else:
                field.render_kw = {'class': 'form-field'}


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
    submit = SubmitField('Сохранить', render_kw={'class': 'submit-button'})


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
    submit = SubmitField('Сохранить', render_kw={'class': 'submit-button'})


class SchoolForm(FlaskForm):
    name = StringField('Название учебного заведения', validators=[DataRequired()])
    course = StringField('Название пройденного курса', validators=[DataRequired()])
    start = DateField('Начало учебы')
    finish = DateField('Завершение учебы')
    certificate = FileField('Полученный сертификат', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Сохранить', render_kw={'class': 'submit-button'})


class ContactForm(FlaskForm):
    phone = StringField('Мобильный телефон')
    email = StringField('Электронная почта', validators=[Email()])
    telegram = StringField('Telegram')
    sn_profile = StringField('Личный сайт или профиль в соцсетях')
    submit = SubmitField('Сохранить', render_kw={'class': 'submit-button'})
