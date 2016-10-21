# flask-minicurso # flask-minicurso


### Criar virtualenv

    pyvenv venv


### Adicionar virtualenv no .gitingore

    echo 'venv' > .gitignore

### Clonar repositório

    git clone https://github.com/I-am-Gabi/flask-minicurso.git

### Instalar requirements

    pip install -r requirements.txt


### Criar database

    sqlite3 pokemons.db < schema.sql 

### Mudar path do database no arquivo minicurso-flask.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////[SEU PATH]]/minicurso-flask/personagens.db'

    