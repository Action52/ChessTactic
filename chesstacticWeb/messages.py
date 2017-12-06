from protorpc import messages
from protorpc import message_types

class MessageNone(messages.Message):
    inti = messages.StringField(1)
# Input messages
#Recibe el token para validar
class Token(messages.Message):
    tokenint = messages.StringField(1, required=True)
    #entityKey = messages.StringField(2, required=False)
    #fromurl = messages.StringField(3)

#Recibe el token y un entityKey de cualquier base de datos para validar
class TokenKey(messages.Message):
    tokenint = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    #fromurl = messages.StringField(3)

#Recibe el email y contrasena para la creacion de token
class EmailPasswordMessage(messages.Message):
    email = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)

# Output messages
#regresa un token
class TokenMessage(messages.Message):
    code = messages.IntegerField(1)
    message = messages.StringField(2)
    token = messages.StringField(3)

#regresa mensajes de lo ocurrido
class CodeMessage(messages.Message):
    code = messages.IntegerField(1)
    message = messages.StringField(2)

#USERS
class UserInput(messages.Message):
    token = messages.StringField(1)
    empresa_key = messages.StringField(2)
    email = messages.StringField(3)
    password = messages.StringField(4)

class UserUpdate(messages.Message):
    token = messages.StringField(1)
    email = messages.StringField(2)
    password = messages.StringField(3)
    entityKey = messages.StringField(4, required=True)

class UserList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(UserUpdate, 2, repeated=True)


######Empresa########

#Mensaje de Entrada y Salida para la base de datos Empresa
class EmpresaInput(messages.Message):
    token = messages.StringField(1, required=True)
    codigo_empresa = messages.StringField(2)
    nombre_empresa = messages.StringField(3)


class EmpresaUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    codigo_empresa = messages.StringField(3)
    nombre_empresa = messages.StringField(4)

#regresa una lista para la base de datos Empresa
class EmpresaList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo EmpresaUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(EmpresaUpdate, 2, repeated=True)

######Tactic########

#Mensaje de Entrada y Salida para Tweets
class TacticInput(messages.Message):
    token = messages.StringField(1, required=True)
    title = messages.StringField(2)
    description = messages.StringField(3)
    category = messages.StringField(5)
    solution = messages.StringField(6)
    urlImage = messages.StringField(7)


class TacticUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    title = messages.StringField(3)
    description = messages.StringField(4)
    category = messages.StringField(5)
    solution = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class TacticList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(TacticUpdate, 2, repeated=True)


######Biography########

#Mensaje de Entrada y Salida para Tweets
class BiographyInput(messages.Message):
    token = messages.StringField(1, required=True)
    title = messages.StringField(2)
    description = messages.StringField(3)
    yearborn = messages.StringField(5)
    yeardead = messages.StringField(6)
    urlImage = messages.StringField(7)


class BiographyUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    title = messages.StringField(3)
    description = messages.StringField(4)
    yearborn = messages.StringField(5)
    yeardead = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class BiographyList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(BiographyUpdate, 2, repeated=True)



######Blog########

#Mensaje de Entrada y Salida para Tweets
class BlogInput(messages.Message):
    token = messages.StringField(1, required=True)
    title = messages.StringField(2)
    description = messages.StringField(3)
    author = messages.StringField(5)
    date = messages.StringField(6)
    urlImage = messages.StringField(7)


class BlogUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    title = messages.StringField(3)
    description = messages.StringField(4)
    author = messages.StringField(5)
    date = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class BlogList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(TacticUpdate, 2, repeated=True)



######Tactic########

#Mensaje de Entrada y Salida para Tweets
class OpeningInput(messages.Message):
    token = messages.StringField(1, required=True)
    title = messages.StringField(2)
    description = messages.StringField(3)
    movements = messages.StringField(5)
    players = messages.StringField(6)
    urlImage = messages.StringField(7)


class OpeningUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    title = messages.StringField(3)
    description = messages.StringField(4)
    movements = messages.StringField(5)
    players = messages.StringField(6)
    urlImage = messages.StringField(7)

#regresa una lista para la base de datos Empresa
class OpeningList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(TacticUpdate, 2, repeated=True)

########Product########

#Mensaje de Entrada y Salida para Tweets
class ProductInput(messages.Message):

    token = messages.StringField(1, required=True)
    code = messages.StringField(2)
    description = messages.StringField(3)
    urlImage = messages.StringField(5)

class ProductUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    #empresa_key = messages.StringField(2, required=True)
    entityKey = messages.StringField(2, required=True)
    code = messages.StringField(3)
    description = messages.StringField(4)
    urlImage = messages.StringField(5)

#regresa una lista para la base de datos Empresa
class ProductList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(ProductUpdate, 2, repeated=True)
