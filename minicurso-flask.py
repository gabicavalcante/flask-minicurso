import random

from flask import Flask, request, render_template
from sqlalchemy import func

from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/gabriela/Documents/developer/minicurso-cientec/minicurso-flask/pokemons.db'
db = SQLAlchemy(app)

ataques = {1: 'ataque1', 2: 'ataque2', 3: 'ataque3'}
current_player = None
players = []

class Pokemons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    forca = db.Column(db.String(50))
    inteligencia = db.Column(db.String(50))
    rapidez = db.Column(db.String(50))

    def __init__(self, nome, forca, inteligencia, rapidez):
        self.nome = nome
        self.forca = forca
        self.inteligencia = inteligencia
        self.rapidez = rapidez

    def __repr__(self):
        return '<Pokemon %r>' % self.nome


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        p = Pokemons(form.nome.data, form.forca.data, form.inteligencia.data, form.rapidez.data)
        db.session.add(p)
        db.session.commit()
    return render_template('index.html', form=form, pokemons=Pokemons.query.all())


@app.route('/play')
def play():
    players = Pokemons.query.all()
    current_player = random.choice(players)
    players.remove(current_player)
    return render_template('game.html', players=players, ataques=ataques, current_player=current_player)


@app.route('/go', methods=['GET', 'POST'])
def go():
    global players
    alvo = request.form.getlist('alvo')
    ataque = request.form.getlist('ataque')
    if not players:
        players = Pokemons.query.all()
        current_player = random.choice(players)
        players.remove(current_player)
    else:
        current_player = random.choice(players)
        players.remove(current_player)
    return render_template('game.html', pokemons=players,
                           alvo=alvo, ataques=ataques, ataque=ataque, content=current_player)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    form = RegistrationForm(request.form)

    if request.method == "POST":
        id = int(request.form['id'])
        db.session.delete(Pokemons.query.get(id))
        db.session.commit()
    return render_template('players.html', players=Pokemons.query.all(), form=form)


@app.route('/players')
def players():
    form = RegistrationForm(request.form)
    return render_template('players.html', players=Pokemons.query.all(), form=form)


if __name__ == '__main__':
    app.secret_key = 'why would I tell you my secret key?'
    app.run(port=8080, debug=True)
