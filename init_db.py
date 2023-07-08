from models import db, User, Receta
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask('app')

# configurar la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Crear base de datoos
with app.app_context():
    db.create_all()
    # print("estoy fuera del if xd")
    # print("estoy dentro del if o.O")
    admin_username = "admin_uno"
    admin_correo = "admin@dishhub.com"
    admin_nombre = "admin"
    admin_apellido = "uno"
    admin_password = generate_password_hash("rodri", method='sha256')
    admin_rol = "admin"
    admin_uno = User(username=admin_username, correo_user=admin_correo, nombre=admin_nombre, apellido=admin_apellido, password=admin_password, rol=admin_rol)
    db.session.add(admin_uno)
    db.session.commit()