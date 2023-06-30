from flask_sqlalchemy import SQLAlchemy

# Instanciamos SqlAlchemy
db = SQLAlchemy()

#Creamos nuestros modelos(Tablas)
class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(12))

