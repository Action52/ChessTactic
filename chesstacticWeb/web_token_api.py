import endpoints
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from protorpc import remote

import jwt
import time

from CustomExceptions import NotFoundException

from messages import EmailPasswordMessage, TokenMessage, CodeMessage, Token, TokenKey, MessageNone
from messages import EmpresaInput, EmpresaUpdate, EmpresaList
from messages import TacticInput, TacticUpdate, TacticList
from messages import BiographyInput, BiographyUpdate, BiographyList
from messages import BlogInput, BlogUpdate, BlogList
from messages import OpeningInput, OpeningUpdate, OpeningList
from messages import UserInput, UserUpdate, UserList
from messages import ProductInput, ProductUpdate, ProductList

from endpoints_proto_datastore.ndb import EndpointsModel

import models
from models import validarEmail
from models import Empresa, Usuarios, Tactic, Product, Biography, Blog, Opening

###############
# Products
###############
@endpoints.api(name='products_api', version='v1', description='products endpoints')
class ProductsApi(remote.Service):

  ######## Add products ##########
  @endpoints.method(ProductInput, CodeMessage, path='products/insert', http_method='POST', name='products.insert')
  def product_add(cls, request):
    try:
      token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
      user = Usuarios.get_by_id(token['user_id'])

      myProduct = Product()

      if myProduct.product_m(request, user.key) == 0:
        codigo = 1
      else:
        codigo = -3

      message = CodeMessage(code=codigo, message='Product added')

    except jwt.DecodeError:
      message = CodeMessage(code=-2, message='Invalid token')
    except jwt.ExpiredSignatureError:
      message = CodeMessage(code=-1, message='Token expired')

    return message

  @endpoints.method(TokenKey, ProductList, path='products/get', http_method='POST', name='products.get')
  def product_get(cls, request):
    try:

      token = jwt.decode(request.tokenint, 'secret')  #checa token
      productentity = ndb.Key(urlsafe = request.entityKey)
      product = Product.get_by_id(productentity.id()) #obtiene usuario

      lista = []  #crea lista
      lstMessage = ProductList(code=1) # crea objeto mensaje
      lista.append(ProductUpdate(token='',
                                 entityKey= product.entityKey,
                                 #empresa_key = user.empresa_key.urlsafe(),
                                 code = product.code,
                                 description = product.description,
                                 urlImage = product.urlImage)) # agrega a la lista

      lstMessage.data = lista #ASIGNA a la salida la lista
      message = lstMessage

    except jwt.DecodeError:
      message = UserList(code=-1, data=[]) #token invalido

    except jwt.ExpiredSignatureError:
      message = UserList(code=-2, data=[]) #token expiro

    return message


######## list products ##########

  @endpoints.method(Token, ProductList, path='products/list', http_method='POST', name='products.list')
  def product_list(cls, request):
    try:

      token = jwt.decode(request.tokenint, 'secret')  #checa token
      user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
      lista = []  #crea lista
      lstMessage = ProductList(code=1) # crea objeto mensaje
      lstBd = Product.query().fetch() # recupera de base de datos

      for i in lstBd: # recorre
        lista.append(ProductUpdate(token='', entityKey = i.entityKey,
                                #empresa_key=user.empresa_key.urlsafe(),
                                code = i.code,
                                description = i.description,
                                urlImage = i.urlImage)) # agrega a la lista

      lstMessage.data = lista # la manda al messa
      message = lstMessage #regresa

    except jwt.DecodeError:
      message = ProductList(code=-1, data=[]) #token invalido
    except jwt.ExpiredSignatureError:
      message = ProductList(code=-2, data=[]) #token expiro
    return message

  @endpoints.method(ProductUpdate, CodeMessage, path='products/update', http_method='POST', name='products.update')
  #siempre lleva cls y request
  def product_update(cls, request):
    try:
      token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
      user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      product = Product()

      # empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
      if product.product_m(request, user.key) == 0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
        codigo = 1

      else:
        codigo = -3
        #la funcion josue_m puede actualizar e insertar
        #depende de la ENTRADA de este endpoint method

      message = CodeMessage(code = 1, message='Sus cambios han sido guardados exitosamente')
    except jwt.DecodeError:
      message = CodeMessage(code = -2, message='Invalid token')
    except jwt.ExpiredSignatureError:
      message = CodeMessage(code = -1, message='Token expired')
    return message

  @endpoints.method(TokenKey, CodeMessage, path='products/delete', http_method='POST', name='products.delete')
  #siempre lleva cls y request
  def product_remove(cls, request):

    try:

      token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      productEntity = ndb.Key(urlsafe = request.entityKey)#Obtiene el elemento dado el EntitKey
      productEntity.delete()#BORRA
      message = CodeMessage(code = 1, message = 'Succesfully deleted')

    except jwt.DecodeError:
      message = CodeMessage(code = -2, message = 'Invalid token')

    except jwt.ExpiredSignatureError:
      message = CodeMessage(code = -1, message = 'Token expired')

    return message

###############
# Usuarios
###############
@endpoints.api(name='usuarios_api', version='v1', description='usuarios endpoints')
class UsuariosApi(remote.Service):
###############get the info of one########
 @endpoints.method(TokenKey, UserList, path='users/get', http_method='POST', name='users.get')
 def users_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   userentity = ndb.Key(urlsafe=request.entityKey)
   user = Usuarios.get_by_id(userentity.id()) #obtiene usuario
            #user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lista.append(UserUpdate(token='',
    entityKey= user.entityKey,
    #empresa_key = user.empresa_key.urlsafe(),
    email = user.email))
   lstMessage.data = lista#ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message


########################## list###################
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
  @endpoints.method(Token, UserList, path='users/list', http_method='POST', name='users.list')
  def lista_usuarios(cls, request):
    try:
      token = jwt.decode(request.tokenint, 'secret')  #checa token
      user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
      lista = []  #crea lista
      lstMessage = UserList(code=1) # crea objeto mensaje
      lstBd = Usuarios.query().fetch() # recupera de base de datos

      for i in lstBd: # recorre
        lista.append(UserUpdate(token='',
        entityKey=i.entityKey,
        #empresa_key=user.empresa_key.urlsafe(),
        email=i.email)) # agrega a la lista

      lstMessage.data = lista # la manda al messa
      message = lstMessage #regresa

    except jwt.DecodeError:
      message = UserList(code=-1, data=[]) #token invalido
    except jwt.ExpiredSignatureError:
      message = UserList(code=-2, data=[]) #token expiro

    return message

  @endpoints.method(TokenKey, CodeMessage, path='users/delete', http_method='POST', name='users.delete')
  #siempre lleva cls y request
  def user_remove(cls, request):
    try:

      token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      usersentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
      usersentity.delete()#BORRA
      message = CodeMessage(code=1, message='Succesfully deleted')

    except jwt.DecodeError:
      message = CodeMessage(code=-2, message='Invalid token')

    except jwt.ExpiredSignatureError:
      message = CodeMessage(code=-1, message='Token expired')

    return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
  @endpoints.method(UserInput, CodeMessage, path='users/insert', http_method='POST', name='users.insert')
  def user_add(cls, request):
    try:
      token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
      user = Usuarios.get_by_id(token['user_id'])

      if validarEmail(request.email) == False: #checa si el email esta registrado
                       #empresakey = ndb.Key(urlsafe=request.empresa_key) #convierte el string dado a entityKey
        if user.usuario_m(request, user.empresa_key) == 0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
          codigo = 1

        else:
          codigo = -3
                         #la funcion josue_m puede actualizar e insertar
                         #depende de la ENTRADA de este endpoint method
        message = CodeMessage(code = codigo, message = 'Succesfully added')

      else:
        message = CodeMessage(code = -4, message = 'El email ya ha sido registrado')

    except jwt.DecodeError:
      message = CodeMessage(code = -2, message = 'Invalid token')

    except jwt.ExpiredSignatureError:
      message = CodeMessage(code = -1, message = 'Token expired')

    return message


##login##

 @endpoints.method(EmailPasswordMessage, TokenMessage, path='users/login', http_method='POST', name='users.login')
 def users_login(cls, request):
  try:
   user = Usuarios.query(Usuarios.email == request.email).fetch() #obtiene el usuario dado el email
   if not user or len(user) == 0: #si no encuentra user saca
    raise NotFoundException()
   user = user[0]
   keye = user.empresa_key.urlsafe() # regresa como mensaje el empresa key
   if not user.verify_password(request.password): # checa la contrasena
    raise NotFoundException()

   token = jwt.encode({'user_id': user.key.id(), 'exp': time.time() + 43200}, 'secret') #crea el token
   message = TokenMessage(token=token, message=keye, code=1) # regresa token
  except NotFoundException:
   message = TokenMessage(token=None, message='Wrong username or password', code=-1)
  return message

##update##
# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserUpdate, CodeMessage, path='user/update', http_method='POST', name='user.update')
#siempre lleva cls y request
 def user_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   if user.usuario_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Empresa
###########################

## Google Cloud Endpoint
@endpoints.api(name='empresas_api', version='v1', description='empresas REST API')
class EmpresasApi(remote.Service):


# get one

 @endpoints.method(TokenKey, EmpresaList, path='empresa/get', http_method='POST', name='empresa.get')
#siempre lleva cls y request
 def empresa_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   empresaentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #empresaentity.get().empresa_key.urlsafe() para poder optener el EntityKey
     ##### ejemplo real
    ####### message = EmpresaList(code=1, data=[EmpresaUpdate(token='Succesfully get', nombre_empresa=empresaentity.get().nombre_empresa, empresa_key=empresaentity.get().empresa_key.urlsafe(), entityKey=empresaentity.get().entityKey)])
   message = EmpresaList(code=1, data = [EmpresaUpdate(token='Succesfully get',
    entityKey = empresaentity.get().entityKey,
    codigo_empresa=empresaentity.get().codigo_empresa,
    nombre_empresa = empresaentity.get().nombre_empresa)])

  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message




 @endpoints.method(TokenKey, CodeMessage, path='empresa/delete', http_method='POST', name='empresa.delete')
#siempre lleva cls y request
 def empresa_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   empresaentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   empresaentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


# insert
 @endpoints.method(EmpresaInput, CodeMessage, path='empresa/insert', http_method='POST', name='empresa.insert')
#siempre lleva cls y request
 def empresa_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario models.py
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0:
    codigo=1
   else:
		codigo=-3
      	      #la funcion josue_m puede actualizar e insertar
	      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Succesfully added')
      #else:
	    #  message = CodeMessage(code=-4, message='Succesfully added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(EmpresaUpdate, CodeMessage, path='empresa/update', http_method='POST', name='empresa.update')
#siempre lleva cls y request
 def empresa_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      #empresakey = ndb.Key(urlsafe=request.empresa_key)#convierte el string dado a entityKey
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, EmpresaList, path='empresa/list', http_method='POST', name='empresa.list')
#siempre lleva cls y request
 def empresa_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   #if user.importante==1 or user.importante==2:
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = EmpresaList(code=1) #CREA el mensaje de salida
   lstBdEmpresa = Empresa.query().fetch() #obtiene de la base de datos
   for i in lstBdEmpresa: #recorre la base de datos
             #inserta a la lista creada con los elementos que se necesiten de la base de datos
             #i.empresa_key.urlsafe() obtiene el entityKey
	     #lista.append(ClientesUpdate(token='', nombre=i.nombre, status=i.status, empresa_key=i.empresa_key.urlsafe(), entityKey=i.entityKey))
    lista.append(EmpresaUpdate(token='',
     entityKey = i.entityKey,
     codigo_empresa=i.codigo_empresa,
     nombre_empresa = i.nombre_empresa))

   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
      #else:
      #    message = EmpresaList(code=-3, data=[])
  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message


###########################
#### Tactics
###########################

@endpoints.api(name='tactic_api', version='v1', description='Tactics REST API')
class TacticApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, TacticList, path='tactic/get', http_method='POST', name='tactic.get')
#siempre lleva cls y request
 def tactic_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   tacticentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = TacticList(code=1, data=[TacticUpdate(token='Succesfully get',
    entityKey=tacticentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(),
    title=tacticentity.get().title,
    description=tacticentity.get().description,
    category=tacticentity.get().category,
    solution=tacticentity.get().solution,
    urlImage=tacticentity.get().urlImage)])
  except jwt.DecodeError:
   message = TacticList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TacticList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='tactic/delete', http_method='POST', name='tactic.delete')
#siempre lleva cls y request
 def tactic_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   tacticentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   tacticentity.delete()#BORRA
   message = CodeMessage(code=0, message='tactic deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, TacticList, path='tactic/list', http_method='POST', name='tactic.list')
#siempre lleva cls y request
 def tactic_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = TacticList(code=1) #CREA el mensaje de salida
   lstBd = Tactic.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey

    lista.append(TacticUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title,
     description=i.description,
     category=i.category,
     solution=i.solution,
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = TacticList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TacticList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TacticInput, CodeMessage, path='tactic/insert', http_method='POST', name='tactic.insert')
#siempre lleva cls y request
 def tactic_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mytactic = Tactic()
   if mytactic.tactic_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Tactic added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TacticUpdate, CodeMessage, path='tactic/update', http_method='POST', name='tactic.update')
#siempre lleva cls y request
 def tactic_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mytactic = Tactic()
   if mytactic.tactic_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='tactic updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Biographies
###########################

@endpoints.api(name='biography_api', version='v1', description='Biographies REST API')
class BiographyApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, BiographyList, path='biography/get', http_method='POST', name='biography.get')
#siempre lleva cls y request
 def biography_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   biographyentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = BiographyList(code=1, data=[BiographyUpdate(token='Succesfully get',
    entityKey=biographyentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(),
    title=biographyentity.get().title,
    description=biographyentity.get().description,
    yearborn=biographyentity.get().yearborn,
    yeardead=biographyentity.get().yeardead,
    urlImage=biographyentity.get().urlImage)])
  except jwt.DecodeError:
   message = BiographyList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = BiographyList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='biography/delete', http_method='POST', name='biography.delete')
#siempre lleva cls y request
 def biography_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   biographyentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   biographyentity.delete()#BORRA
   message = CodeMessage(code=0, message='biography deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, BiographyList, path='biography/list', http_method='POST', name='biography.list')
#siempre lleva cls y request
 def biography_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = BiographyList(code=1) #CREA el mensaje de salida
   lstBd = Biography.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey

    lista.append(BiographyUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title,
     description=i.description,
     yearborn=i.yearborn,
     yearend=i.yearend,
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = BiographyList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = BiographyList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(BiographyInput, CodeMessage, path='biography/insert', http_method='POST', name='biography.insert')
#siempre lleva cls y request
 def tactic_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myBiography = Biography()
   if myBiography.biography_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Biography added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(BiographyUpdate, CodeMessage, path='biography/update', http_method='POST', name='biography.update')
#siempre lleva cls y request
 def biography_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myBiography = Biography()
   if myBiography.biography_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='tactic updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



###########################
#### Blogs
###########################

@endpoints.api(name='blog_api', version='v1', description='Blogs REST API')
class BlogApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, BlogList, path='blog/get', http_method='POST', name='blog.get')
#siempre lleva cls y request
 def blog_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   blogentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = BlogList(code=1, data=[BlogUpdate(token='Succesfully get',
    entityKey=blogentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(),
    title=blogentity.get().title,
    description=tacticentity.get().description,
    author=tacticentity.get().author,
    date=tacticentity.get().date,
    urlImage=tacticentity.get().urlImage)])
  except jwt.DecodeError:
   message = BlogList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = BlogList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='blog/delete', http_method='POST', name='blog.delete')
#siempre lleva cls y request
 def blog_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   blogentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   blogentity.delete()#BORRA
   message = CodeMessage(code=0, message='blog deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, BlogList, path='blog/list', http_method='POST', name='blog.list')
#siempre lleva cls y request
 def blog_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = BlogList(code=1) #CREA el mensaje de salida
   lstBd = Blog.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey

    lista.append(TacticUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title,
     description=i.description,
     author=i.author,
     date=i.date,
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = BlogList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = BlogList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(BlogInput, CodeMessage, path='blog/insert', http_method='POST', name='blog.insert')
#siempre lleva cls y request
 def blog_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myblog = Blog()
   if myblog.blog_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Blog added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(BlogUpdate, CodeMessage, path='blog/update', http_method='POST', name='blog.update')
#siempre lleva cls y request
 def blog_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myblog = Blog()
   if myblog.blog_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Blog updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



###########################
#### Openings
###########################

@endpoints.api(name='opening_api', version='v1', description='Openings REST API')
class OpeningApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, OpeningList, path='opening/get', http_method='POST', name='opening.get')
#siempre lleva cls y request
 def opening_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   openingentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = OpeningList(code=1, data=[OpeningUpdate(token='Succesfully get',
    entityKey=openingentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(),
    title=openingentity.get().title,
    description=openingentity.get().description,
    movements=openingentity.get().movements,
    players=openingentity.get().players,
    urlImage=openingentity.get().urlImage)])
  except jwt.DecodeError:
   message = OpeningList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = OpeningList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='opening/delete', http_method='POST', name='opening.delete')
#siempre lleva cls y request
 def opening_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   openingentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   openingentity.delete()#BORRA
   message = CodeMessage(code=0, message='Opening deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, OpeningList, path='opening/list', http_method='POST', name='opening.list')
#siempre lleva cls y request
 def opening_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = OpeningList(code=1) #CREA el mensaje de salida
   lstBd = Opening.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey

    lista.append(TacticUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title,
     description=i.description,
     movements=i.movements,
     players=i.players,
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = OpeningList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = OpeningList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(OpeningInput, CodeMessage, path='opening/insert', http_method='POST', name='opening.insert')
#siempre lleva cls y request
 def opening_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myOpening = Opening()
   if myOpening.opening_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Opening added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(OpeningUpdate, CodeMessage, path='opening/update', http_method='POST', name='opening.update')
#siempre lleva cls y request
 def opening_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myOpening = Opening()
   if myOpening.opening_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Opening updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


application = endpoints.api_server([UsuariosApi, EmpresasApi, TacticApi, BiographyApi, BlogApi, OpeningApi, ProductsApi], restricted=False)
