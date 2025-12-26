from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, DateField, SubmitField, TextAreaField, IntegerField, BooleanField, PasswordField)
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange


class BaseForm:
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


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-field login-field'})
    password = PasswordField(
        'Пароль', validators=[DataRequired()], render_kw={'class': 'form-field login-field'})
    submit = SubmitField('Войти или зарегистрироваться', render_kw={'class': 'submit-button'})


class ResumeForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()], render_kw={'class': 'form-field'})
    submit = SubmitField('Создать', render_kw={'class': 'submit-button'})


class PersonalForm(BaseForm, FlaskForm):
    image = FileField('Ваша фотография', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    gender = SelectField('Пол', choices=[('male', 'мужской'), ('female', 'женский')], default='male')
    birthdate = DateField('Дата рождения')
    location = StringField('Местоположение')
    citizenship = StringField('Гражданство')
    about = TextAreaField('О себе')


class SpecializationForm(BaseForm, FlaskForm):
    readiness = SelectField(
        'Готовность к работе',
        choices=[('not_looking', 'не ищу работу'), ('looking', 'ищу работу'), ('consider', 'рассмотрю предложения')],
        default='0',
    )
    salary = IntegerField('Ожидаемое вознаграждение', validators=[
        InputRequired(),
        NumberRange(min=1, message='Введите положительное целое число'),
    ])
    slogan = StringField('Коротко о себе')
    specialization = SelectField(
        'Специализация',
        choices=[
            ('development', 'Разработка'),
            ('testing', 'Тестирование'),
            ('analytics', 'Аналитика'),
            ('design', 'Дизайн'),
            ('management', 'Менеджмент'),
            ('security', 'Информационная безопасность'),
            ('ai', 'Искусственный интеллект'),
        ],
        default='development',
        validators=[DataRequired()],
    )
    grade = SelectField(
        'Ваша квалификация',
        choices=[
            ('no', 'не указана'),
            ('intern', 'стажёр'),
            ('junior', 'младший'),
            ('middle', 'средний'),
            ('senior', 'старший'),
            ('lead', 'ведущий'),
        ],
        default='no',
        validators=[DataRequired()],
    )
    skills = TextAreaField('Профессиональные навыки', validators=[DataRequired()])
    languages = StringField('Знание языков')
    remote_ready = BooleanField('Готов к удаленной работе')
    relocation_ready = BooleanField('Готов к переезду')


class JobForm(BaseForm, FlaskForm):
    name = StringField('Название компании', validators=[DataRequired()])
    location = StringField('Местоположение компании')
    specialization = SelectField(
        'Специализация',
        choices=[
            ('development', 'Разработка'),
            ('testing', 'Тестирование'),
            ('analytics', 'Аналитика'),
            ('design', 'Дизайн'),
            ('management', 'Менеджмент'),
            ('security', 'Информационная безопасность'),
            ('ai', 'Искусственный интеллект'),
        ],
        default='development',
        validators=[DataRequired()],
    )
    grade = SelectField(
        'Квалификация',
        choices=[
            ('no', 'не указана'),
            ('intern', 'стажёр'),
            ('junior', 'младший'),
            ('middle', 'средний'),
            ('senior', 'старший'),
            ('lead', 'ведущий'),
        ],
        default='no',
        validators=[DataRequired()],
    )
    position = StringField('Ваша должность в компании')
    start = DateField('Начало работы')
    finish = DateField('Окончание работы')
    about = TextAreaField('Ваши обязанности и достижения')
    skills = TextAreaField('Применяемые вами навыки')


class SchoolForm(BaseForm, FlaskForm):
    name = StringField('Название учебного заведения', validators=[DataRequired()])
    course = StringField('Название пройденного курса', validators=[DataRequired()])
    start = DateField('Начало учебы')
    finish = DateField('Завершение учебы')


class ContactForm(BaseForm, FlaskForm):
    phone = StringField('Мобильный телефон')
    email = StringField('Электронная почта', validators=[Email()])
    telegram = StringField('Telegram')
    sn_profile = StringField('Личный сайт или профиль в соцсетях')
