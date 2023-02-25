

class Config:
    DEBUG = True
    TESTING = True

    #Config de base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False #podemos cambiar esta configuracion tamb para no tener ning problema(nose bien q hace, averiguar)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/blog_db' # creo q es la forma de simplificar el codigo

# vamos a crear 2 clase mas para modo de producccion y otra para modod de desarrollo

# voy a heredar de la clase (config) toda la configuracion q tiene por defecto. Lo unico q voy a cambiar es el 
# (DEBUG) que esta en True por False, xq cuando esta en modo de produccion ya no tiene que estar en modo de 
# desarrollo, xeso el debug tiene q cambiar de true a fasle
class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config): #aqui si el debug va a estar en true
    #le vamos a colocar un 'key', se llama secretkey, esto nos va a pedir cuando nosotros estemos trabajando 
    # al momento de rendirizar un mensaje de error o un mensaje de seguridad tenemos que tener este key
    DEBUG = True
    SECRET_KEY = 'dev'
# y tamb el testing va a estra en true xq cuando estamos en modod de desarrollo tambien podemos testear 
    TESTING = True
    








