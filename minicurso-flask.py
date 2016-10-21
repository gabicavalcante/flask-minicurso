import random
# http://flask-sqlalchemy.pocoo.org/2.1/queries/
# https://community.nitrous.io/tutorials/set-up-a-python-flask-application-with-sqlite
from flask import Flask, request, render_template
import logging

from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/gabriela/Documents/developer/minicurso-cientec/minicurso-flask/personagens.db'
db = SQLAlchemy(app)

ataques = {10: 'ataque1', 20: 'ataque2', 30: 'ataque3'}
players = []
current_player = None


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
    global players, current_player

    players = Personagens.query.all()
    current_player = random.choice(players)
    players.remove(current_player)
    return render_template('game.html', opts=players, ataques=ataques, current_player=current_player.nome)


@app.route('/go', methods=['GET', 'POST'])
def go():
    global players, current_player

    ataque = int(request.form.getlist('ataque')[0])
    alvo = Personagens.query.filter_by(nome=request.form.getlist('alvo')[0]).first()
    alvo.vida -= ataque
    p = Personagens.query.filter_by(nome=current_player.nome).first()
    p.xp += ataque

    if not players:
        players = Personagens.query.all()

    current_player = random.choice(players)
    players.remove(current_player)
    opt = list(db.session.query(Personagens))
    app.logger.info(opt)
    app.logger.info(current_player)
    opt.remove(current_player)

    # app.logger.info(current_player)
    return render_template('game.html', opts=opt, players=Personagens.query.all(),
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
