from myblog import db

# para crear un modelo simplemente vamos a crear una clase y esta clase la vamos a 
# convertir en un modelo de base de datos 

class User(db.Model): #esta clase va a heredar del modelo de sqlalchemy y nuestra clase ya es un modelo
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50))
    password = db.Column(db.Text)

# ahora para luego reutilizar esta clase como por ejemplo para crear el usuario
# crear el usuario y todo eso vamos a crear un constructor.

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

# y luego de eso para representar como se va a mostrar este objeto tamb podemos usar en este caso
# el metodo __repr__ el cual va a devolver un string

    def __repr__(self) -> str:

        return f'User: {self.username}'




# si nosotros colocamos o pasamos algunos atribitos, en la base de datos lo va a tomar 
# o lo va a colocar esta clase como un modelo y el nombre de la tabla lo va a colocar 
# con nombre user en pura minuscula.. ahora si queremos modificaar el nombre de la tabla
# normalmente en bd se coloca en plural, entonces colocamos __tablename__ y este va a ser igual a 
# 'users' en plural. aqui estamos mostrando como se va a colocar o mostrar el nombre de la tabla
# ahora le vamos a colocqar las columnas, en este caso van a pasar simplemente a ser los 
# atributos de una clase

