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

@app.route("/register", methods = ["POST", "GET"])
def register():
    #Recibimos los datos del Front
    if request.method == 'POST':
        username = request.form ["username"]
        email = request.form ["correo_user"]
        password = request.form ["password"]
        nombre = request.form ["nombre"]
        apellido = request.form ["apellido"]
        
        usuario = User(username, email, password, nombre, nombre, apellido)
        #Agregamos a la db
        #Agrego con
        db.session.add(usuario)
        #Y confirmo con
        db.session.commit()

        #Ver como era
        #global current_user
        #current_user = id_usuario
        return 'Registrado correctamente'
    return render_template ("register.html")


@app.route("/agregar")
def hello_world():
    usuario_agregar = User(usuario='Rodri', password='132')
    db.session.add(usuario_agregar)
    db.session.commit()
    return 'se agrego correctamente'


## Breakpoint ##
if __name__ == "__main__":
    app.run (debug=True)
