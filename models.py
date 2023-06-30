from flask_sqlalchemy import SQLAlchemy

# Instanciamos SqlAlchemy
db = SQLAlchemy()

#Creamos nuestros modelos(Tablas)
class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(12))
    correo_user = db.Column(db.String, unique = True, nullable = False)
    #foto_usuario no se como poner en una db

class Receta(db.Model):
    id_receta = db.Column(db.Integer, primary_key=True)
    nombre_receta = db.Column(db.String(12), unique=True, nullable=False)
    descripcion_receta = db.Column(db.String(12))

    #Iterar la lista de ingredientes dps