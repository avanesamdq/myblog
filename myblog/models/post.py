
from myblog import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column( db.Integer, primary_key= True)
    author = db.Column( db.Integer, db.ForeignKey('users.id'), nullable = False )
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    im = db.Column(db.String(100), nullable=True)
    
    # lo sasque de aca para la actualizacion pero aca no cambie nada y de aca fui a la vista de blog en la funcion actualizar



    def __init__(self, author, title, body, im) -> None:
        self.author = author
        self.title = title
        self.body = body
        self.im = im

    def __repr__(self) -> str:

        return f'Post: {self.title}'



"""  Con esto ya tenemos construidos nuestros modelos, ahora lo que vamos hacer 
es construir nuestras vistas, xq desde las vistas es donde vamos a reutilizar los
modelos donde vamos a realizar la conexion, capturar la peticion del cliente y 
responder al cliente...
    Otra cosa: En la carpeta (models) como models es un paquete tenemos que crear 
    un archivo ( __init__.py ) con esto le vamos a indicar que model es un paquete."""
