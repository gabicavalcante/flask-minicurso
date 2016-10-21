#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from flask import Flask, request, render_template, flash, redirect, url_for
import logging

from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/kessiacastro/Dev/flask-pyladies/flask-minicurso/personagens.db'
db = SQLAlchemy(app)

ataques = {10: 'ataque1', 20: 'ataque2', 30: 'ataque3'}
players = []
current_player = None
opts = []


class Personagens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    xp = db.Column(db.Integer)
    vida = db.Column(db.Integer)
    forca = db.Column(db.Integer)
    inteligencia = db.Column(db.Integer)
    rapidez = db.Column(db.Integer)

    def __init__(self, nome, xp, vida, forca, inteligencia, rapidez):
        self.nome = nome
        self.xp = xp
        self.vida = vida
        self.forca = forca
        self.inteligencia = inteligencia
        self.rapidez = rapidez

    def __repr__(self):
        return '<Personagem %r>' % self.nome

    def __eq__(self, other):
        if not isinstance(other, Personagens):
            return False

        return (self.id == other.id)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        p = Personagens(form.nome.data, 10, 100, form.forca.data, form.inteligencia.data, form.rapidez.data)
        db.session.add(p)
        db.session.commit()
    return render_template('index.html', form=form, personagens=Personagens.query.all())


@app.route('/play')
def play():
    global players, current_player, opts
    players = Personagens.query.all()
    for player in players:
        player.vida = 100
        player.xp = 10
        db.session.add(player)
        db.session.commit()

    current_player = random.choice(players)
    opts = list(players)
    opts.remove(current_player)
    return render_template('game.html', opts=opts, ataques=ataques, current_player=current_player.nome)


@app.route('/go', methods=['GET', 'POST'])
def go():
    global players, current_player, opts

    players = db.session.query(Personagens).filter(Personagens.vida > 0).all()
    ataque = int(request.form.getlist('ataque')[0])
    alvo = Personagens.query.filter_by(nome=request.form.getlist('alvo')[0]).first()

    # Retira o personagem com 0 de vida da rodada
    if alvo.vida - ataque <= 0:
        players.remove(alvo)
        # Se um dois dois finalistas morrer o jogo acaba
        if len(players) < 2:
            flash("Game Over!")
            return redirect(url_for('hello_world'))
    else:
        alvo.vida -= ataque
    p = Personagens.query.filter_by(nome=current_player.nome).first()
    p.xp += ataque
    db.session.add(alvo)
    db.session.add(p)
    db.session.commit()

    # Função para escolher um player random diferente do current_player
    def randomPlayer():
        random_player = random.choice(players)
        while random_player == current_player:
            random_player = random.choice(players)
        return random_player

    current_player = randomPlayer()
    # Filtra os opts somente por personagens ainda com vida e retira o current da lista
    opts = list(db.session.query(Personagens).filter(Personagens.vida > 0))
    opts.remove(current_player)
    app.logger.info(opts)
    app.logger.info(current_player)

    return render_template('game.html', opts=opts, players=players,
                           alvo=alvo.nome, ataques=ataques, ataque=ataque, current_player=current_player.nome)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    form = RegistrationForm(request.form)

    if request.method == "POST":
        id = int(request.form['id'])
        db.session.delete(Personagens.query.get(id))
        db.session.commit()
    return render_template('players.html', players=Personagens.query.all(), form=form)


@app.route('/players')
def players():
    form = RegistrationForm(request.form)
    return render_template('players.html', players=Personagens.query.all(), form=form)


if __name__ == '__main__':
    app.secret_key = 'why would I tell you my secret key?'
    app.run(port=8080, debug=True)
