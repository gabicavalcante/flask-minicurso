# coding=utf-8
from wtforms import Form, StringField, validators, IntegerField, SelectMultipleField


class RegistrationForm(Form):
    nome = StringField('nome', [validators.Length(min=4, max=25)])
    forca = IntegerField('forca')
    inteligencia = IntegerField('inteligencia')
    rapidez = IntegerField('rapidez')
