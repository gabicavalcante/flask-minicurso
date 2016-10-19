# coding=utf-8
from wtforms import Form, StringField, validators, IntegerField, SelectMultipleField

my_choices = [('1', 'forca'), ('2', 'inteligencia'), ('3', 'rapidez')]

class RegistrationForm(Form):
    nome = StringField('nome', [validators.Length(min=4, max=25)])
    skill = IntegerField('skill')