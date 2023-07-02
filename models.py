from flask_sqlalchemy import SQLAlchemy

# Instanciamos SqlAlchemy
db = SQLAlchemy()

#Creamos nuestros modelos(Tablas)
class User(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    correo_user = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String(12))
    nombre = db.Column(db.String(12))
    apellido = db.Column(db.String(12))
    receta = db.relationship('Receta', backref = 'user')

    def __init__ (self, username, correo_user, password, nombre,apellido):
        self.username = username
        self.correo_user = correo_user
        self.password = password
        self.nombre = nombre
        self.apellido = apellido

class Receta(db.Model):
    id_receta = db.Column(db.Integer, primary_key=True)
    nombre_receta = db.Column(db.String(25))
    descripcion_receta = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__ (self, nombre_receta, descripcion_receta, user_id):
        self.nombre_receta = nombre_receta
        self.descripcion_receta = descripcion_receta
        self.user_id = user_id

    #calificacion_receta = db.Column(db.Integer)
    #fecha_receta = db.Column(db.String)
#Lista de ingredientes despues para la db