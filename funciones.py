from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from models import Receta

def permiso_para_modificar_receta(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        receta_id = kwargs.get('receta_id')

        # Verificar si la receta existe en la base de datos
        receta = Receta.query.get(receta_id)
        if not receta:
            return redirect(url_for('home')) # Devuelve al home


        if receta.id != current_user.id and not receta.es_usuario_colaborativo(current_user.username) and not current_user.rol('admin'):
            flash('La receta no existe o no tienes permisos para editar') 
            return redirect(url_for('home')) # Devuelve al home

        return func(*args, **kwargs)

    return decorador

def permiso_para_eliminar_receta(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        receta_id = kwargs.get('receta_id')

        # Verificar si la receta existe en la base de datos
        receta = Receta.query.get(receta_id)
        if not receta:
            flash('La receta no existe o no tienes permisos para editar')  # Devuelve un error 404 Not Found si la receta no existe
            return redirect(url_for('home')) # Devuelve al home

        if receta.id != current_user.id and current_user.rol != 'admin':
            flash('La receta no existe o no tienes permisos para editar')  # 
            return redirect(url_for('home')) # Devuelve al home
        return func(*args, **kwargs)

    return decorador
