import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import images
from google.appengine.ext import blobstore
import cloudstorage
import mimetypes
import json
import os
import jinja2

from models import Empresa
from models import Tactic
from models import Biography
from models import Blog
from models import Opening

jinja_env = jinja2.Environment(
 loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class DemoClass(object):
 pass

def MyClass(obj):
 return obj.__dict__


class GetTacticsHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe()
     myEmpKey = ndb.Key(urlsafe=strKey)
     myTactics = Tactic.query(Tactic.empresa_key == myEmpKey)

     myList = []
     for i in myTactics:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.category = i.category
      myObj.solution = i.solution
      myObj.urlImage = i.urlImage
      myList.append(myObj)

     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)


class GetBiographiesHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe()
     myEmpKey = ndb.Key(urlsafe=strKey)
     myBiography = Biography.query(Biography.empresa_key == myEmpKey)

     myList = []
     for i in myBiography:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.yearborn = i.yearborn
      myObj.yeardead = i.yeardead
      myObj.urlImage = i.urlImage
      myList.append(myObj)

     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

class GetBlogsHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe()
     myEmpKey = ndb.Key(urlsafe=strKey)
     myBlog = Blog.query(Blog.empresa_key == myEmpKey)

     myList = []
     for i in myBlog:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.author = i.author
      myObj.date = i.date
      myObj.urlImage = i.urlImage
      myList.append(myObj)

     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)


class GetOpeningsHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe()
     myEmpKey = ndb.Key(urlsafe=strKey)
     myOpening = Opening.query(Opening.empresa_key == myEmpKey)

     myList = []
     for i in myOpening:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.movements = i.movements
      myObj.players = i.players
      myObj.urlImage = i.urlImage
      myList.append(myObj)

     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

###########################################################################


class UpHandler(webapp2.RequestHandler):
    def _get_urls_for(self, file_name):

     bucket_name = app_identity.get_default_gcs_bucket_name()
     path = os.path.join('/', bucket_name, file_name)
     real_path = '/gs' + path
     key = blobstore.create_gs_key(real_path)
     try:
      url = images.get_serving_url(key, size=0)
     except images.TransformationError, images.NotImageError:
      url = "http://storage.googleapis.com{}".format(path)

     return url


    def post(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     bucket_name = app_identity.get_default_gcs_bucket_name()
     uploaded_file = self.request.POST.get('uploaded_file')
     file_name = getattr(uploaded_file, 'filename', None)
     file_content = getattr(uploaded_file, 'file', None)
     real_path = ''

     if file_name and file_content:
      content_t = mimetypes.guess_type(file_name)[0]
      real_path = os.path.join('/', bucket_name, file_name)

      with cloudstorage.open(real_path, 'w', content_type=content_t,
       options={'x-goog-acl': 'public-read'}) as f:
       f.write(file_content.read())

      key = self._get_urls_for(file_name)
      self.response.write(key)


class LoginHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('login2.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)


class TacticHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('tactic.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class BiographyHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('biography.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class BlogHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('blog.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)


class OpeningHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('opening.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)


class MainHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('index.html', template_context))


   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/tactics', TacticHandler),
    ('/biographies', BiographyHandler),
    ('/blogs', BlogHandler),
    ('/openings', OpeningHandler),
    ('/up', UpHandler),
    ('/getTactics', GetTacticsHandler),
    ('/getBiographies', GetBiographiesHandler),
    ('/getBlogs', GetBlogsHandler),
    ('/getOpenings', GetOpeningsHandler),
], debug = True)
