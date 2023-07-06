#Importancion de librerias  
from flask import Flask, redirect, render_template, request, render_template, request, redirect, url_for, flash
# Importamos los modelos de la tablas
from models import db, User, Receta
# Importamos funciones de flask-login
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
# Importamos funcion hasheadora para mayor seguridad
from werkzeug.security import generate_password_hash
#Importamos fechas
from datetime import datetime
import os


fecha_string = datetime.strftime(datetime.now(), '%b %d, %Y')


# Instanciamos Flask
app = Flask(__name__, static_folder='uploads')


app.config['UPLOAD_FOLDER'] = 'uploads'


# Configuraciones para la base de datos
### Ver para implementar variable de entorno .env
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SuperSecretKeyxD'


# Inicializamos la base de datos
db.init_app(app)


# Instanciamos LoginManager para conectar con la app
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Ruta de landing page
@app.route("/")
def index():
    return 'Logeate en /login o crea tu cuenta en /register'


#Ruta donde se ven todas las recetas
@app.route("/home")
def home():
    recetas = Receta.query.all()
    # print(recetas)
    return render_template ("home.html",recetas=recetas)


#Ruta para registrarse
@app.route("/register", methods=["POST", "GET"])
def register():
    # Recibimos los datos del Front
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("correo_user")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        # Hacemos la confirmación de creación de usuario
        if User.query.filter_by(username=username).first():
            flash('Este usuario ya existe uwu', category='error')
        elif User.query.filter_by(correo_user=email).first():
            flash('Este correo ya existe uwu', category='error')
        elif len(username) < 4:
            flash('Tu nombre de usuario debe ser mayor a 4 caracteres', category='error')
        elif len(email) < 4:
            flash('Tu correo debe ser mayor a 4 caracteres', category='error')
        elif len(nombre) < 4:
            flash('Tu nombre debe ser mayor a 4 caracteres', category='error')
        elif len(apellido) < 4:
            flash('Tu apellido debe ser mayor a 4 caracteres', category='error')
        elif len(password1) < 3:
            flash('Tu contraseña debe ser mayor a 3 caracteres', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden', category='error')
        else:
            # Hasheamos la contraseña para mayor seguridad
            password = generate_password_hash(password1, method='sha256')
            user = User(username=username, correo_user=email, password=password, nombre=nombre, apellido=apellido)
            # Agregamos a la db
            db.session.add(user)
            # Y confirmamos
            db.session.commit()
            # Recuerda que el usuario esta logeado
            login_user(user, remember=True)
            flash('Usuario creado!', category='success')
            
            return redirect(url_for("home"))
    return render_template("register.html")


#Ruta para logearte
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_user = request.form.get("correo_user")
        password = request.form.get("password")
        user = User.query.filter_by(correo_user=correo_user).first()
        if user and user.confirmar_contraseña(password):
            flash('Logeado correctamente', category='succes')
            # Recuerda que el usuario esta logeado
            login_user(user, remember=True)
            print(current_user)
            return redirect(url_for('home'))  
        else:
            flash('Correo o contraseña incorrecta')

    return render_template('login.html')


# Creamos una funcion para manejar los usuarios logeados
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Ruta para cerrar session
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#Ruta donde se ve la receta seleccionada
@app.route("/recipe/<id>")
@login_required
def recipe(id):
    receta_buscada = Receta.query.get(id)
    # lista_ingredientes = receta_buscada.ingredientes.split(",")
    # print(lista_ingredientes)
    return render_template ("recipe.html", receta_buscada=receta_buscada)


#Ruta para crear nueva receta
@app.route("/recipe_new", methods=["POST", "GET"])
@login_required
def recipe_new():
    if request.method == 'POST':
        nombre_receta = request.form.get("nombre_receta")
        descripcion_receta = request.form.get("descripcion_receta")
        ingredientes = request.form.get("ingredientes")
        colaboradores = 'mauri'
        user_id = current_user.id
        file = request.files['image']
        
        # Verifica si se proporcionó un archivo
        if file:
            # Genera el nombre de archivo combinando el nombre de la receta y el ID de la receta
            filename = f'{nombre_receta}_{current_user.id}.jpg'  # Cambia la extensión según el formato de imagen que desees
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Guarda el archivo en el directorio de uploads
            image_path = os.path.join('/uploads', filename)
        else:
            # Si no se proporcionó un archivo, establece el image_path como None o una ruta predeterminada según tus necesidades
            image_path = None
        
        receta_de_usuario = Receta(nombre_receta=nombre_receta, descripcion_receta=descripcion_receta, ingredientes=ingredientes, user_id=user_id, colaboradores=colaboradores, image_path=image_path)
        db.session.add(receta_de_usuario)
        db.session.commit()
        
        return redirect(url_for("your_recipes"))
    
    return render_template("recipe_new.html")


#Ruta para ver tus recetas
@app.route("/your_recipes")
@login_required
def your_recipes():
    query_recetas = Receta.query.filter_by(user_id=current_user.id).all()
    return render_template ("your_recipes.html", query_recetas=query_recetas)


#Ruta para editar una receta
@app.route("/recipe_edit/<id>", methods=['POST', 'GET'])
@login_required
def recipe_edit(id):
    receta = Receta.query.get(id)
    if request.method == 'POST':
        receta.nombre_receta = request.form['nombre_receta']
        receta.descripcion_receta = request.form['descripcion_receta']
        receta.ingredientes = request.form['ingredientes']
        db.session.commit()
        return redirect(url_for("your_recipes"))
    #lista_ingredientes = receta.ingredientes.split(",")
    return render_template ("recipe_edit.html", receta=receta) #lista_ingredientes=lista_ingredientes)


#Ruta donde se eliminan las recetas
@app.route("/recipe_del/<id>")
@login_required
def recipe_del(id):
    receta = Receta.query.get(id)
    db.session.delete(receta)
    db.session.commit()
    return redirect (url_for("your_recipes"))


## Breakpoint ##
if __name__ == "__main__":
    app.run (debug=True)
