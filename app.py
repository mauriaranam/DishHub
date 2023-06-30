#Importancion de librerias  
from flask import Flask, render_template, request
# Importamos los modelos de la tablas
from models import db, User

app = Flask(__name__)


# configurar la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos
db.init_app(app)

@app.route("/")
def index():
    return render_template("home.html")

#@app.route("/register", methods = ["POST", "GET"])
#def register():
#    if request.method == 'POST':


@app.route("/agregar")
def hello_world():
    usuario_agregar = User(usuario='Rodri', password='132')
    db.session.add(usuario_agregar)
    db.session.commit()
    return 'se agrego correctamente'


## Breakpoint ##
if __name__ == "__main__":
    app.run (debug=True)
