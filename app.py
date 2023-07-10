#Importancion de librerias  
from flask import Flask, redirect, render_template, request, render_template, request, redirect, url_for, flash
# Importamos los modelos de la tablas
from models import db, User, Receta
# Importamos funciones de flask-login
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
# Importamos funcion hasheadora para mayor seguridad
from werkzeug.security import generate_password_hash
import os
# Importamos la libreria datetime
from datetime import datetime
# importamos nuestras funciones creadas
from funciones import permiso_para_modificar_receta, permiso_para_eliminar_receta, permiso_para_colaboraciones, modo_admin
# Para modificar tamaño de las imagenes
from PIL import Image
import re
# Importamos openai
import openai
openai.api_key = "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"


# Instanciamos Flask
app = Flask(__name__, static_folder='static')


app.config['UPLOAD_FOLDER'] = 'static/uploads'

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


# Creamos una funcion para manejar los usuarios logeados
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Ruta de landing page
@app.route("/")
def index():
    return redirect(url_for('home'))


#Ruta donde se ven todas las recetas
@app.route("/home")
def home():
    recetas = Receta.query.all()
    return render_template ("home.html",recetas=recetas)


#Ruta para AlexIA
@app.route("/alexia", methods=["POST", "GET"])
def buscar_alexia():
    if request.method == 'POST':
        ingredientes_usuario = request.form.get("ingredientes")
        prompt = """
        Instrucciones para AlexIA:
        1. Responde únicamente consultas relacionadas con recetas de cocina, ingredientes y preparaciones.
        2. Si el usuario pregunta sobre cualquier otro tema, no proporciones una respuesta y muestra un mensaje indicando que AlexIA solo responde consultas culinarias.
        3. Provee información detallada y precisa sobre las recetas solicitadas.
        4. Si el usuario solicita inspiración, recomienda platos populares o ofrece sugerencias basadas en preferencias de ingredientes.
        5. Si el usuario solicita una receta específica, proporciona los ingredientes necesarios y los pasos de preparación de manera clara y organizada.
        6. Si el usuario tiene alguna pregunta técnica sobre técnicas culinarias, proporciona explicaciones claras y consejos útiles.
        7. Utiliza un tono amigable y cercano para interactuar con los usuarios.
        8. Siempre verifica la comprensión de la consulta del usuario antes de proporcionar una respuesta.
        9. Siempre saluda
        10. Si el usuario solo ingresa ingredientes, brinda recetas con los ingredientes disponibles
        Chef AlexIA: {pregunta}
        """
        pregunta = f"{ingredientes_usuario}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt.format(pregunta=pregunta),
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.3
        )
        # Obtener la respuesta generada por el modelo
        respuesta = response.choices[0].text.strip()
        # Procesa la respuesta y muestra los resultados al usuario
        return render_template("alexia.html", respuesta=respuesta, chef_nombre="AlexIA")
    return render_template("alexia.html", chef_nombre="AlexIA")


#Ruta para la busqueda dentro de la base de datos por ingredientes(Recetas)
@app.route("/solicitud", methods=['POST', 'GET'])
def solicitar_recetas():
    pedido = request.form.get("pedido")
    recetas = buscar_recetas_db(f"%{pedido}%")
    recetas_db = None
    if pedido:
        recetas_db = buscar_recetas_db(pedido)
    return render_template("solicitud.html", recetas=recetas, recetas_db=recetas_db)
def buscar_recetas_db(ingredientes):
    recetas = Receta.query.filter(Receta.ingredientes.ilike(f"%{ingredientes}%")).all()
    return recetas


#Ruta para registrarse
@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        flash(f'Ya estas logeado {current_user.nombre}! :)')
        return redirect(url_for('home'))
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Ya estas logeado {current_user.nombre}! :)')
        return redirect(url_for('home'))
    if request.method == 'POST':
        correo_user = request.form.get("correo_user")
        password = request.form.get("password")
        user = User.query.filter_by(correo_user=correo_user).first()
        if user and user.confirmar_contraseña(password):
            flash(f'Bienvenidx de vuelta {user.nombre} :)', category='succes')
            # Recuerda que el usuario esta logeado
            login_user(user, remember=True)
            print(current_user)
            return redirect(url_for('home'))  
        else:
            flash('Correo o contraseña incorrecta', category='error')
    return render_template('login.html')


@app.route("/admin", methods=['GET', 'POST'])
@login_required
@modo_admin
def admin():
    users = User.query.all()
    print(users)
    print(f'ID DEL USER {current_user.username}')
    return render_template("admin.html", users=users)


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
    receta = Receta.query.get(id)
    
    username_colaborador = [name.strip() for name in receta.colaboradores.split(',')]
    colaboradores = User.query.filter(User.username.in_(username_colaborador)).all()
    # print(receta.image_path)
    return render_template ("recipe.html", receta=receta, colaboradores=colaboradores)


#Ruta para crear nueva receta
@app.route("/recipe_new", methods=["POST", "GET"])
@login_required
def recipe_new():
    users = User.query.filter(User.username != current_user.username and User.username != 'admin_uno').all()
    if request.method == 'POST':
        nombre_receta = request.form.get("nombre_receta")
        descripcion_receta = request.form.get("descripcion_receta")
        ingredientes = request.form.get("ingredientes")
        colaborador = request.form.get('colaborador')
        if colaborador == 'sin_colaborador':
            colaborador = ','
            pass
        user_id = current_user.id
        file = request.files['image']    
        fecha_actual = datetime.strftime(datetime.now(), '%d, %b, %Y')
        privacidad = True
        # Verifica si se proporcionó un archivo
        if file:
            # Genera el nombre de archivo combinando el nombre de la receta y el ID de la receta
            filename = f'{nombre_receta}_{current_user.id}.jpg'  # Cambia la extensión según el formato de imagen que desees
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Ruta completa para el archivo
            # Redimensionar la imagen al formato deseado (1080x1080)
            desired_image_size = (1080, 1080)
            image = Image.open(file)
            image = image.resize(desired_image_size)
            
            # Guardar la imagen redimensionada
            image.save(filepath)
            # Almacena el path en la dB
            image_path = os.path.join('/static/uploads', filename)
        else:
            # Si no se proporcionó un archivo, establece el image_path como None o una ruta predeterminada según tus necesidades
            image_path = None
        receta_de_usuario = Receta(nombre_receta=nombre_receta, descripcion_receta=descripcion_receta, ingredientes=ingredientes, user_id=user_id, colaboradores=colaborador, image_path=image_path, fecha_receta=fecha_actual, privacidad=privacidad)
        db.session.add(receta_de_usuario)
        db.session.commit()
        return redirect(url_for("your_recipes"))
    return render_template("recipe_new.html", users=users)


#Ruta para ver tus recetas
@app.route("/your_recipes")
@login_required
def your_recipes():
    query_recetas = Receta.query.filter_by(user_id=current_user.id).all()
    return render_template ("your_recipes.html", query_recetas=query_recetas)


#Ruta para ver la receta de otro
@app.route("/recipes_of/<id_usuario>")
@login_required
def recipe_of_user(id_usuario):
    usuario = User.query.get(id_usuario)
    print('nooo')
    if usuario:
        print('siiii')
        query_recetas = Receta.query.filter_by(user_id=usuario.id).all()
        return render_template ("recipes_of.html", query_recetas=query_recetas, usuario=usuario)
    else:
        flash('Este usuario no existe :s', category='error')
        return redirect(url_for('home')) # Devuelve al home


#Ruta para editar una receta
@app.route("/recipe_edit/<receta_id>", methods=['POST', 'GET'])
@login_required
@permiso_para_modificar_receta
def recipe_edit(receta_id):
    receta = Receta.query.get(receta_id)
    users = User.query.filter(User.username != current_user.username and User.username != 'admin_uno').all()
    print(receta)
    
    if receta:
        if request.method == 'POST':
            receta.nombre_receta = request.form['nombre_receta']
            receta.descripcion_receta = request.form['descripcion_receta']
            receta.ingredientes = request.form['ingredientes']
            colaborador = request.form.get('colaborador')
            if colaborador == 'sin_colaborador':
                print('sin colaborador')
                pass
            elif not receta.es_usuario_colaborativo(colaborador):
                receta.colaboradores += f",{colaborador}"
                db.session.commit()
            file = request.files['image']
            # Verifica si se proporcionó un archivo
            if file:
                # Genera el nombre de archivo combinando el nombre de la receta y el ID de la receta
                filename = f'{receta.nombre_receta}_{current_user.id}.jpg'  # Cambia la extensión según el formato de imagen que desees
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Guarda el archivo en el directorio de uploads
                image_path = os.path.join('/static/uploads', filename)
                receta.image_path = image_path
            else:
                # Si no se proporcionó un archivo, establece el image_path como None o una ruta predeterminada según tus necesidades
                image_path = None
            privacidad = request.form.get("privacidad")
            if privacidad == "publica":
                receta.privacidad = True
            elif privacidad == "privada":
                receta.privacidad = False
            db.session.commit()
            return redirect(url_for('home'))

    else:
        flash('La receta no existe', category='error')
        return redirect(url_for('home'))
    return render_template("recipe_edit.html", receta=receta, users=users)


# Ruta para ver colaboradores
@app.route('/colaboradores/<receta_id>', methods=['POST', 'GET'])
@login_required
@permiso_para_colaboraciones
def colaboradores(receta_id):
    receta = Receta.query.get(receta_id)
    users = User.query.filter(User.username != current_user.username and User.username != 'admin_uno').all()
    colaboradores = []
    if receta:
        print(receta.id)
        username_colaborador = [name.strip() for name in receta.colaboradores.split(',')]
        colaboradores = User.query.filter(User.username.in_(username_colaborador)).all()
        return render_template("colaboradores.html", receta=receta, colaboradores=colaboradores, users=users)
    
    else:
        flash('No existe esta receta', category='error')
        return redirect(url_for('home'))


#Ruta para agregar colaboradores
@app.route('/colaboradores/<receta_id>/agregar', methods=['POST'])
@login_required
@permiso_para_colaboraciones
def agregar_colaborador(receta_id):
    receta = Receta.query.get(receta_id)
    print(receta)
    
    username_a_agregar = request.form.get("username")
    if username_a_agregar == 'sin_colaborador':
            print('sin colaborador')
            flash('sin cambios', category='error')
            return redirect(url_for('colaboradores', receta_id=receta.id))
            
    if receta:
        if current_user.username == username_a_agregar:
            flash('no te podes agregar a vos mismo jaja', category='error')
            return redirect(url_for('colaboradores', receta_id=receta.id))
        elif not receta.es_usuario_colaborativo(username_a_agregar):
            receta.colaboradores += f",{username_a_agregar}"
            db.session.commit()
            flash(f"Se agregó a {username_a_agregar} como colaborador", category="success")
            return redirect(url_for('colaboradores', receta_id=receta.id))
        else:
            flash(f"{username_a_agregar} ya es colaborador de esta receta", category="error")
            return redirect(url_for('colaboradores', receta_id=receta.id))
    else:
        flash("La receta no existe", category="error")
        return redirect(url_for('home'))


#Ruta para eliminar colaboradores
@app.route('/colaboradores/eliminar/<receta_id>/<username>')
@login_required
@permiso_para_colaboraciones
def eliminar_colaborador(receta_id, username):
    receta = Receta.query.get(receta_id)
    if receta:
        if current_user.username == username:
            flash('no te podes eliminarte a vos mismo jaja')
            return redirect(url_for('colaboradores', receta_id=receta.id))
        if receta.es_usuario_colaborativo(username):
            colaboradores = [name.strip() for name in receta.colaboradores.split(",")]
            colaboradores = [name for name in colaboradores if name != username]
            receta.colaboradores = ",".join(colaboradores)
            db.session.commit()
            flash(f"{username} Dejo de ser colaborador", category="success")
            return redirect(url_for('colaboradores', receta_id=receta.id))
            
        else:
            flash(f"{username} no es un colaborador de esta receta", category="error")
            return redirect(url_for('colaboradores', receta_id=receta.id))
    else:
        flash("La receta no existe", category="error")
        return redirect(url_for('home'))


#Ruta donde se eliminan las recetas
@app.route("/recipe_del/<receta_id>")
@permiso_para_eliminar_receta
@login_required
def recipe_del(receta_id):
    receta = Receta.query.get(receta_id)
    db.session.delete(receta)
    db.session.commit()
    flash('Receta eliminada correctamente', category='success')
    return redirect (url_for("your_recipes"))


#Ruta para editar un usuario
@app.route("/user_edit/<id>", methods=['POST', 'GET'])
@login_required
@modo_admin
def user_edit(id):
    user = User.query.get(id)
    print(user)
    if user:
        if request.method == 'POST':
            user.username = request.form['username']
            user.nombre = request.form['nombre']
            user.apellido = request.form['apellido']
            user.rol = request.form['rol']
            db.session.commit()
            print(user)
            return redirect(url_for("admin"))
    else:
        flash('El usuario no existe', category='error')
        return redirect(url_for('admin'))
    return render_template("user_edit.html", user=user)


#Ruta donde se eliminan los usuarios
@app.route("/user_del/<id>")
@modo_admin
@login_required
def user_del(id):
    User.query.filter_by(id=id).delete()
    Receta.query.filter_by(user_id=id).delete()
    db.session.commit()
    flash('Usuario eliminado correctamente', category='success')
    return redirect (url_for("admin"))


## Breakpoint ##
if __name__ == "__main__":
    app.run (debug=True)    