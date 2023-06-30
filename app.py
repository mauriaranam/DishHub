#Importacion de Librerias
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

#Creamos la app y el modelo de la base de Datos (Hacer eso que hicimos el otro dia de poner en otro lado, no me recuerdo como era bro jsjsjs)
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos.db'
app.config ['SECRET_KEY'] = 'puni77'
