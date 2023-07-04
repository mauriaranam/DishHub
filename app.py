#Importancion de librerias  
from flask import Flask, redirect, render_template, request, render_template, request, redirect, url_for
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
        usuario = User(username=username, correo_user=email, password=password, nombre=nombre,apellido=apellido)
        #Agregamos a la db
        #Agrego con
        db.session.add(usuario)
        #Y confirmo con
        db.session.commit()
        global current_user
        current_user = usuario.id
        print(current_user)
        return redirect(url_for("login"))
    return render_template ("register.html")

@app.route("/recipe_new", methods=["POST", "GET"])
def recipe_new():
    if request.method == 'POST':
        nombre_receta = request.form.get("nombre_receta")
        descripcion_receta = request.form.get("descripcion_receta")
        ingredientes = request.form.get("ingredientes")
        global current_user 
        user_id = current_user
        receta_de_usuario = Receta(nombre_receta=nombre_receta,descripcion_receta=descripcion_receta,ingredientes=ingredientes, user_id=user_id)
        db.session.add(receta_de_usuario)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template ("recipe_new.html")


#Ruta donde se ven todas las recetas
@app.route("/home")
def home():
    recetas = Receta.query.all()
    print(recetas)
    return render_template ("home.html",recetas=recetas)

#Ruta para editar una receta
@app.route("/recipe_edit")
def recipe_edit():
    return render_template ("recipe_edit.html")

#Ruta donde se eliminan las recetas
@app.route("/recipe_del")
def recipe_del():
    pass

#Ruta donde se ve la receta seleccionada
@app.route("/recipe/<id>")
def recipe(id):
    receta_buscada = Receta.query.get(id)
    lista_ingredientes = receta_buscada.ingredientes.split(",")
    print(lista_ingredientes)
    return render_template ("recipe.html", receta_buscada=receta_buscada, lista_ingredientes=lista_ingredientes)

@app.route("/your_recipes")
def your_recipes():
    render_template ("your_recipes.html")

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
