#Importancion de librerias  
from flask import Flask, render_template, request, redirect, url_for
# Importamos los modelos de la tablas
from models import db, User, Receta

app = Flask(__name__)


# configurar la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos
db.init_app(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    #Recibimos los datos del Front
    if request.method == 'POST':
        username = request.form ["username"]
        email = request.form ["correo_user"]
        password = request.form ["password"]
        nombre = request.form ["nombre"]
        apellido = request.form ["apellido"]
        usuario = User(username=username, correo_user=email, password=password, nombre=nombre, apellido=apellido)
        #Agregamos a la db
        #Agrego con
        db.session.add(usuario)
        #Y confirmo con
        db.session.commit()
        global current_user
        current_user = User.id
        return redirect(url_for("login"))
    return render_template ("register.html")

@app.route("/receta", methods=["POST", "GET"])
def receta():
    #Recibimos los datos del Front
    if request.method == 'POST':
        nombre_receta = request.form ["nombre_receta"]
        descripcion_receta = request.form ["descripcion_receta"]
        global current_user 
        user_id = current_user
        receta_de_usuario = Receta(nombre_receta=nombre_receta,descripcion_receta=descripcion_receta, user_id=user_id)
        db.session.add(receta_de_usuario)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template ("receta.html")


@app.route("/home")
def home():
    return render_template ("home.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_user = request.form ['correo_user']
        password = request.form ['password']
        usuario_db = User.query.filter_by(correo_user=correo_user).first()
        if usuario_db is not None:
            if usuario_db.password == password:
                global current_user 
                current_user = usuario_db.id
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        elif usuario_db is None:
            return redirect(url_for('login'))  
    return render_template('login.html')

## Breakpoint ##
if __name__ == "__main__":
    app.run (debug=True)
