from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from models import Receta, User

def permiso_para_modificar_receta(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        receta_id = kwargs.get('receta_id')

        # Verificar si la receta existe en la base de datos
        receta = Receta.query.get(receta_id)
        if not receta:
            flash('La receta no existe', category='error') 
            return redirect(url_for('home')) # Devuelve al home
            
        if receta.user_id == current_user.id or receta.es_usuario_colaborativo(current_user.username) or current_user.rol == 'admin':
            return func(*args, **kwargs)
        
        else:
            flash('no tienes permisos para editar', category='error') 
            return redirect(url_for('home')) # Devuelve al home

    return decorador

def permiso_para_colaboraciones(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        receta_id = kwargs.get('receta_id')

        # Verificar si la receta existe en la base de datos
        receta = Receta.query.get(receta_id)
        if not receta:
            flash('La receta no existe para modificar', category='error')  # Devuelve un error 404 Not Found si la receta no existe
            return redirect(url_for('home')) # Devuelve al home

        if receta.user_id == current_user.id or current_user.rol == 'admin':
            return func(*args, **kwargs)
        else:
            print(f'id receta: {receta.user_id}, id current user: {current_user.id}')
            flash('no tienes permisos para modificar', category='error')  # 
            return redirect(url_for('home')) # Devuelve al home
    return decorador


def permiso_para_eliminar_receta(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        receta_id = kwargs.get('receta_id')
        # Verificar si la receta existe en la base de datos
        receta = Receta.query.get(receta_id)
        if not receta:
            flash('La receta no existe para eliminar', category='error')  # Devuelve un error 404 Not Found si la receta no existe
            return redirect(url_for('home')) # Devuelve al home
        if receta.user_id == current_user.id or current_user.rol == 'admin':
            return func(*args, **kwargs)
        else:
            flash('No tienes los permisos para eliminar', category='error')
            return redirect (url_for('home'))
    return decorador

def modo_admin(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        id = kwargs.get('id')
        # Verificar si la receta existe en la base de datos
        user = User.query.get(id)
        if current_user.rol == 'admin':
            return func(*args, **kwargs)
        else:
            flash('no tienes los permisos', category='error') 
            return redirect(url_for('home')) # Devuelve al home
    return decorador

