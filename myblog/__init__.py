
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# cargar las configuraciones
# el from_objet es xq trabajamos con clases y estod son objetos
app.config.from_object('config.DevelopmentConfig') #el nombre del archivo(config), y el nombre de la clase(DevelopmentConfig)
db = SQLAlchemy(app)

# IMPORTAR VISTAS 
from myblog.views.auth import auth # importando mi blueprint auth
#registrar mi blueprint en mi aplicacion
app.register_blueprint(auth)


from myblog.views.blog import blog # importamos el blueprint que se llama blog
#ahora vamso a registrar
app.register_blueprint(blog) #le registramos qui nuesro blueprint que es blog


db.create_all()

