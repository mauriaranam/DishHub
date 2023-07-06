from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime

# Instanciamos SqlAlchemy
db = SQLAlchemy()

#Fecha actual en string
fecha_string = datetime.strftime(datetime.now(), '%b %d, %Y')

#Creamos nuestros modelos(Tablas) y usamos UserMixin para usar las propiedades de flask-login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    correo_user = db.Column(db.String, unique = True, nullable = False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    password = db.Column(db.String(400))
    rol = db.Column(db.String(15), default='gastronomo') # Hacemos que el rol default sea gastronomo
    recetas = db.relationship('Receta', backref = 'user')

    # Funcion que te permite confirmar contraseñá hasheada
    def confirmar_contraseña(self, password):
        return check_password_hash(self.password, password)


class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_receta = db.Column(db.String(50))
    descripcion_receta = db.Column(db.Text)
    ingredientes = db.Column(db.Text)
    colaboradores = db.Column(db.String(400)) #Almacena los colaboradores
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Creador de la receta
    fecha_receta = db.Column(db.String, default=fecha_string)
    image_path = db.Column(db.String(200), nullable=True)  # Almacena la ruta de la imagen


    # Comprueba si un nombre de usuario se encuentra en la lista de colaboradores
    def es_usuario_colaborativo(self, username):
        colaboradores = [name.strip() for name in self.colaboradores.split(',')]
        return username in colaboradores

    #calificacion_receta = db.Column(db.Integer) Agregar al terminar todo