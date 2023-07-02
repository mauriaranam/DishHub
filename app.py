#Importancion de librerias  
from flask import Flask, redirect, render_template, request
# Importamos los modelos de la tablas
from models import db, User

app = Flask(__name__)


# configurar la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route(('/login'))
def login():
    return render_template('login.html')

@app.route(('/register'))
def register():
    return render_template('register.html')


## Breakpoint ##
if __name__ == "__main__":
    app.run (debug=True)
