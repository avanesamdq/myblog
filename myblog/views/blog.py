

from flask import render_template, Blueprint, flash, g, redirect, request,url_for

# tamb para manejar el error, en este caso para manejar el error vamos a importar de 
# werkzeug.exceptions
from werkzeug.exceptions import abort 
from myblog.models.post import Post
from myblog.models.user import User
# tamb vamos a utilizar el login required que hemos creado en el auth, necesitabas esta
# funcion xq xjemp: para registrar un blog o para publicar o editar un blog necesita q un ususario este logeado
from myblog.views.auth import login_required
# tamb para trabajar con las bases de datos importaremos el db que creamos en el init del paquete principal
from myblog import db
from datetime import datetime
#Para subir archivo tipo foto al servidor 
from myblog import app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/myblog/static/arch'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# registrar en blueprint

blog = Blueprint('blog', __name__)

# crear funcion para obtener un ususario mediante el id
# OBTENER UN USUARIO
def get_user(id):
    user= User.query.get_or_404(id)
    return user

# LISTAR TODOS LOS POST 
@blog.route('/') # esto va a arrancar desde inicio
def index():
    posts = Post.query.all() # con esto ya tenemos todos los posts
    #hacer un for para recorrer los post 


    #print(image_64_encode)


    posts = list(reversed(posts))
    db.session.commit() # para generar el cambio que estamos generando
    return render_template('blog/index.html', posts = posts, get_user = get_user)# aqui hemos reendirizado simplemente un template, pero tamb vamos a devolver un data
    # vamos a reendirizar lo q esta en blog(si vamos a la carpeta de templates,vamos a ver que hay una con nombre blog),
    # y que se llama index.html, luego de la coma, vamos a enviar toda la data en forma de diccionario,
    # le pasamos la clave (posts), y el contenido va hacer posts.

# REGISTRAR O CREAR UNA PUBLICACION 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blog.route('/blog/create', methods = ('GET','POST'))
@login_required #con esta funcion vamos a enviar esta vista y tiene q estar logeado un usuario para realizar esta accion y si no esta logeado esta accion simplemente estara deshabilitada
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        im = request.form.get('file')#toma la foto desde el formulario

        #________________________________ cod nuev ______________________
        # compruebe si la solicitud de publicación tiene la parte del archivo
        #if 'file' not in request.files:
           # flash('Sin parte de archivo')
           # return redirect(request.url)
        #file = request.files['file']
        # Si el usuario no selecciona un archivo, el navegador envía un
        # archivo vacío sin nombre de archivo.
        #if file.filename == '':
           # flash('No selected file')
            #return redirect(request.url)
        #if file and allowed_file(file.filename):
         #   filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          #  return redirect(url_for('download_file', name=filename))


        #______________________________________________________________

        # la variable g.user va a tener el id, colocamos g.user.id.. de esta forma vamos a obtener crear un objeto del tipo post
        # colocando el author, titulo, y el contenido, la fecha se crea automaticamente. 

        post = Post(g.user.id, title, body, im)#aqui tamb hay q enviarle el id el autor, si va a estar logeado...
        #________________________________________________________________
        #________________________________________________________________
        error = None
        if not title:
            error = 'Se requiere un titulo.'
        if error is not None:
            flash(error)
        else: 
            db.session.add(post) #si es nulo vamos a pasar a registrar
            db.session.commit() #para que haga cambios en la base de datos agregamos el commit
            return redirect(url_for('blog.index'))#si todo sale bien lo vamos a redireccionar a la parte de blog
        
        flash(error)
        flash('Publicación enviada correctamente.')

    return render_template('blog/create.html')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



def get_post(id, check_author = True):
    post = Post.query.get(id)
    if post is None:
        abort(404, f'Id {id} de la publicacion no existe')

    if check_author and post.author != g.user.id:
        abort(404)
    return post 

# UPDATE POST
#para actualizar necesitamos obtener el id, ponemos int para recibir ese valor q vamos
#a recibir mediante url a entero. xq todo lo que vamos a recibir mediante url va hacer de
#tipo string, entonces con esto le estamos diciendo q vamos a recibir en tipo entero
@blog.route('/blog/update/<int:id>', methods = ('GET','POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        post.created = datetime.now()

        error = None
        if not post.title:
            error = 'Se requiere un titulo'

        if error is not None:
            flash(error)
        else:
            db.session.add(post)#este add lo que va hacer es agregar un registro y si es q ese registro no tiwnw un id 
#entonces va a crear un nuevo registro, ahora si ese registro o ese post o este objeto q estamos enviando
#tiene un id entonces lo que va hacer es actualizar 
            db.session.commit()
            return redirect(url_for('blog.index'))

        flash(error)
    return render_template('blog/update.html', post = post)#y tamb vamos a enviar un post, aqui
# ya no vamos a enviar una lista sino que vamos a enviar un objeto y este objeto lo vamos a recuperar en cada campo para poder modificar

# ELIMINAR UN POST 

@blog.route('/blog/delete/<int:id>')
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    

    return redirect(url_for('blog.index'))

