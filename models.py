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
    #foto_usuario no se como poner en una db

    def __init__ (self, username, correo_user, password, nombre,apellido):
        self.username = username
        self.correo_user = correo_user
        self.password = password
        self.nombre = nombre
        self.apellido = apellido

class Receta(db.Model):
    id_receta = db.Column(db.Integer, primary_key=True)
    ####id_usuario = db.Column(db.Integer, foreign_key=True)
    nombre_receta = db.Column(db.String(25), unique=True, nullable=False)
    descripcion_receta = db.Column(db.String(25))
    ####ingredientes = db.Column(db.List)
    calificacion_receta = db.Column(db.Integer)
    #foto_receta no se como poner en una db
    fecha_receta = db.Column(db.String)


    #Iterar la lista de ingredientes dsp