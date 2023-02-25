""" aqui lo que vamos hacer es registrar las vistas en este caso de nuestro views,
por ahora lo unico q podriamos hacer es crear una funcion y esta funcion mostrarlo
con una ruta y ya esta. pero aqui vamos a trabajar con ( blueprint ) y tamb dentro 
de aqui vamos a estar utilizando mas herramientas de flask """

# render_template = nos va a servir para rendirizar nuetsros template de las vistas
# blueprint = es para registrar nuestras vistas en nuestra app, practicamente en el __init__.py del paquete principal
# flash = va a flashear algun msj si es que ha habido algun error
# g = el cual va a capturar si algun ususario esta iniciado en sesion o no
# redirect = para redireccionar a alguna ruta 
# request = para capturar la peticion del cliente o lo que nos este enviando el cliente
# session = en este caso para hacer consultas a la base de datos 
# url_for = es practicamente para trabajar con las rutas y redireccionar a otras rutas de nuestra app

import functools
from flask import render_template, Blueprint, flash, g, redirect, request, session,url_for
from myblog.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from myblog import db
# uno es para chequear y el otro para generar 

#crear un blueprint, va a contener todas nuestras vistas.
# esta vista se va a llamar (blueprint('auth')), nombre del archivo ( __name__ ), desde aqui va arrancar nuestro url (url_prefix...)
auth = Blueprint('auth', __name__, url_prefix= '/auth')

# REGISTRAR UN USUARIO 

# esta funcion va a estra decorada con el rout que hemos visto de la app, ahora cuando nosotros trabajmos con
# blueprint ya no vamos a utilizar la app o no es necesario usar la app, xq todas las vistas vamos a 
# crear mediante blueprint y blueprint es el que va a mandar a nuestra aplicacion.

#aqui lo que hemos creado con blueprint(@auth) y vamos a utilizar router y luego vamos a ponere una ruta
# esta ruta va a seguir a url_prefix por ejempli ('/auth') luego de eso '/register', lergo tamb podemos indicar
#con q metodos trabajar, porejm quiero devilver un texto plano, utilizaria un get, pero cuando nosostros ya vamos a tener el template desde donde nos van a enviar un formulario necesitamos el motodo post.
@auth.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username, generate_password_hash(password))

        error = None
        if not username:
            error = 'Se requiere nombre de Usuario.'
        elif not password:
            error = 'Se requiere una Contrasena.'

# colocando query estamos haciendo una consulta  ala base de datos
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'el usuario {username} ya esta registrado'
        flash(error)

# first es para que me filtre un ususario, entonces va a buscar un ususario con el nombre que yo estoy intentando registrar


    # aqui no le puedo pasar simplemente el password asi nada mas xq vamos a encriptarlo.

    return render_template('auth/register.html')
# el render_template puede de hecho recibir varios valores, el primero nuestro archivo html
# entonces tenemos q poner donde se encuentra nuestro archivo html. Flask en este caso va a 
# ir automaticamente a buscar a la carpeta templates y dentro de templates va a buscar entre los archivos html


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INICIAR SESION 
@auth.route('/login', methods = ('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None

        user = User.query.filter_by(username = username).first()

        if user == None:
            error = 'Nombre de usuario no existe.'
        elif not check_password_hash(user.password, password):
            error = 'Contrasena Incorrecta.'

        if error is None:
            session.clear()
            session ['user_id'] = user.id
            return redirect(url_for('blog.index'))
        flash(error)

    return render_template('auth/login.html')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        g.user = User.query.get_or_404(user_id)

''' con esta funcion vamos a capturar si un usuario esta loggeado o no. ponemos (user_id) va a ser igual a
con el metodo session obtenemos con el metodo (get()) el id('user_id').. 
si user_id es nulo, (quiere decir q no esta loggeado), vamos a utilizar el (g.user),
es igual a None, (xq no esta loggeado)..
else: (en caso de que) es practicamente obtener un usuario.
g.user es igual a (=) y aqui lo q vamos a obtener es cargar un usuario el cual este loggeado,
entonces vamos a utilizar nuestro model punto User punto query (User.query), 
y el motodo get y con esto podriamos obtener aqui simplemente colocando el id,
pero para q maneje tamb el error podemos utilizar (get_or_404()) si es q no lo encuentra
nos va a devolver un error y aqui le colocamos el (user_id)...

y ahora para q esta funcion funcione por completo vamos a utilizar de nuestro
blueprint que es el auth, before_app_request..
'''

# CERRAR SESION 
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

#algunos campos como por ejemplo para registrar un block y todo eso van a necesitar
# ser iniciado sesion, creamos una funcion el cual le va a autentificar que se requiere q inice una sesion
# si es q no esta loggeado no puede realizar consultas como editar o eliminar


'''la funcion (login_required) en este caso va a recibir como argumento una vista
xq aqui vamos decorar a esas vistas que necesitan loggearse, aqui vamos a recibir una 
funcion que va hacer practicamente la vista que requieren loggearse..
luego utilizaremos un decorador, este decoradore va a decorar otra funcion
el cual va a verificar si esta loggeado o no y luego de eso va a retornarlo a la parte de 
login si es q no esta loggeado '''

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) # a esa vista tiene q redireccionar
        return view(**kwargs)# y si esta logeado simplemente va a retornar la vista
    return wrapped_view #por ultimo lo q vamos a retornar va hacer la fuincion que va aser decorada o  ala funcion q va a decorar



