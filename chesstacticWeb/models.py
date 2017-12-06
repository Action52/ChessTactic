import base64
import Crypto
from Crypto.Hash import SHA256
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from protorpc import remote
from endpoints_proto_datastore.ndb import EndpointsModel
import endpoints
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers

class CustomBaseModel(EndpointsModel):
    def populate(self, data):
        super(self.__class__, self).__init__()
        for attr in self._message_fields_schema:
            if hasattr(data, attr):
                setattr(self, attr, getattr(data, attr))

## empresa
class Empresa(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'codigo_empresa', 'nombre_empresa')
    codigo_empresa = ndb.StringProperty()
    nombre_empresa = ndb.StringProperty()

       ###Empresa####
    def empresa_m(self, data):
        empresa = Empresa()#Crea una variable de tipo Base de datos
        empresa.populate(data)#Llena la variables con los datos dados por el request en main.py
        #empresa.empresa_key=empresakey #inserta el entityKey de la empresa que es un parametro que se manda en main.py
        empresa.put()#inserta o hace un update depende del main.py
        return 0

#####COMPANIES#########
class Companies(CustomBaseModel):
    _message_fields_schema = ('name', 'address', 'RFC', 'photourl')
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    RFC = ndb.StringProperty()
    photourl = ndb.StringProperty()

#####PROPERTIES#########
class Properties(CustomBaseModel):
    _message_fields_schema = ('latitude',
                              'longitude',
                              'rooms',
                              'bathrooms',
                              'propertyType',
                              'yearBuilt',
                              'squareMeters',
                              'state',
                              'country', 'photourl')

    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()
    rooms = ndb.StringProperty()
    bathrooms = ndb.StringProperty()
    propertyType = ndb.StringProperty()
    yearBuilt = ndb.StringProperty()
    squareMeters = ndb.StringProperty()
    state = ndb.StringProperty()
    country = ndb.StringProperty()
    photourl = ndb.StringProperty()

#####USUARIOS#########

class Usuarios(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'email', 'password', 'salt')

    empresa_key = ndb.KeyProperty(kind=Empresa)
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    salt = ndb.StringProperty(indexed=False)

    def hash_password(self):
        """ Create a cryptographyc random secure salt and hash the password
            using the salt created and store both in the database, the password
            and the salt """
        # Note: It is needed to encode in base64 the salt, otherwise it will
        # cause an exception trying to store non utf-8 characteres
        self.salt = base64.urlsafe_b64encode(
            Crypto.Random.get_random_bytes(16))
        hash_helper = SHA256.new()
        hash_helper.update(self.password + self.salt)
        self.password = hash_helper.hexdigest()

    def verify_password(self, password):
        """ Verify if the password is correct """
        hash_helper = SHA256.new()
        hash_helper.update(password + self.salt)
        return hash_helper.hexdigest() == self.password

       ###Usuarios####
    def usuario_m(self, data, empresakey):
        user = Usuarios()#Crea una variable de tipo Base de datos
        user.populate(data)#Llena la variables con los datos dados por el request en main.py
        user.empresa_key=empresakey
        user.status=1
        user.hash_password()#encripta la contrasena
        user.put()#inserta o hace un update depende del main.py
        return 0

class Product(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'code', 'description', 'urlImage')
    user_key = ndb.KeyProperty(kind=Usuarios)
    code = ndb.StringProperty()
    description = ndb.StringProperty()
    urlImage = ndb.StringProperty()

    def product_m(self, data, userkey):

        product = Product()#Crea una variable de tipo Tweet
        product.populate(data)#Llena la variables con los datos dados por el request en main.py
        product.user_key=userkey#inserta el entityKey de la empresa que es un parametro que se manda en main.py
        product.put()#inserta o hace un update depende del main.py
        return 0

######### Tactics #########

class Tactic(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'title', 'description', 'category', 'solution', 'urlImage')
    empresa_key = ndb.KeyProperty(kind=Empresa)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    category = ndb.StringProperty()
    solution = ndb.StringProperty()
    urlImage = ndb.StringProperty()

    ### Tactic ####
    def tactic_m(self, data, empresakey):
        tactic  = Tactic()#Crea una variable de tipo Tweet
        tactic.populate(data)#Llena la variables con los datos dados por el request en main.py
        tactic.empresa_key=empresakey#inserta el entityKey de la empresa que es un parametro que se manda en main.py
        tactic.put()#inserta o hace un update depende del main.py
        return 0


class Biography(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'title', 'description', 'yearborn', 'yeardead', 'urlImage')
    empresa_key = ndb.KeyProperty(kind=Empresa)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    yearborn = ndb.StringProperty()
    yeardead = ndb.StringProperty()
    urlImage = ndb.StringProperty()

    ### Biography ####
    def biography_m(self, data, empresakey):
        biography  = Biography()#Crea una variable de tipo Tweet
        biography.populate(data)#Llena la variables con los datos dados por el request en main.py
        biography.empresa_key=empresakey#inserta el entityKey de la empresa que es un parametro que se manda en main.py
        biography.put()#inserta o hace un update depende del main.py
        return 0

class Blog(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'title', 'description', 'author', 'date', 'urlImage')
    empresa_key = ndb.KeyProperty(kind=Empresa)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    author = ndb.StringProperty()
    date = ndb.StringProperty()
    urlImage = ndb.StringProperty()

    ### Blog ####
    def blog_m(self, data, empresakey):
        blog  = Blog()#Crea una variable de tipo Tweet
        blog.populate(data)#Llena la variables con los datos dados por el request en main.py
        blog.empresa_key=empresakey#inserta el entityKey de la empresa que es un parametro que se manda en main.py
        blog.put()#inserta o hace un update depende del main.py
        return 0

class Opening(CustomBaseModel):
    _message_fields_schema = ('entityKey', 'title', 'description', 'movements', 'players', 'urlImage')
    empresa_key = ndb.KeyProperty(kind=Empresa)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    movements = ndb.StringProperty()
    players = ndb.StringProperty()
    urlImage = ndb.StringProperty()

    ### Opening ####
    def opening_m(self, data, empresakey):
        opening  = Opening()#Crea una variable de tipo Tweet
        opening.populate(data)#Llena la variables con los datos dados por el request en main.py
        opening.empresa_key=empresakey#inserta el entityKey de la empresa que es un parametro que se manda en main.py
        opening.put()#inserta o hace un update depende del main.py
        return 0

#### create demo

def validarEmail(email):
    emailv = Usuarios.query(Usuarios.email == email)
    if not emailv.get():
        return False
    else:
        return True

#### create root Empresa

"""if validarEmail("leonvillapun@outlook.com") == False:
    empresaAdmin = Empresa(
      codigo_empresa = 'outlook',
      nombre_empresa="Nueva empresa",
    )
    empresaAdmin.put()

#### create root user

    keyadmincol = ndb.Key(urlsafe=empresaAdmin.entityKey)
    admin = Usuarios(
          empresa_key = keyadmincol,
          email="leonvillapun@outlook.com",
          password="1234567",
    )
    admin.hash_password()
    admin.put()"""
