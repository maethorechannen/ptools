import os
import model
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AuthPage(webapp.RequestHandler):
    template_path =  os.path.join(os.path.dirname(__file__), 'templates')
    def get(self):
        user = users.get_current_user()
        if user:
            self.auth_get(user)            
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def post(self):
        user = users.get_current_user()
        if user:
            self.auth_post(user)            
        else:
            self.redirect(users.create_login_url(self.request.uri))
                    

class MainPage(AuthPage):
    def auth_get(self, user):
        path = os.path.join(self.template_path, 'main.html')
        user_podcasts = db.GqlQuery("SELECT * FROM Podcast WHERE owner = :1", user)
        template_values = {
            'user' : user,
            'podcasts' : user_podcasts
        }
        self.response.out.write(template.render(path, template_values))

class CreatePodcast(AuthPage):
    def auth_get(self, user):
        path = os.path.join(self.template_path, 'create_podcast.html')
        template_values = {
            'user' : user
        }
        self.response.out.write(template.render(path, template_values))

    def auth_post(self, user):
        podcast = model.Podcast()
        podcast.owner = user
        podcast.title = self.request.get('title')
        podcast.put()
        self.redirect('/')
        
class EditPodcast(AuthPage):
    def auth_get(self, user):
        path = os.path.join(self.template_path, 'edit_podcast.html')
        template_values = {
            'user' : user
        }
        self.response.out.write(template.render(path, template_values))

class RPCHandler(AuthPage):
    def auth_get(self, user):
        self.response.out.write(simplejson.dumps(user.email()))
        
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/create_podcast', CreatePodcast),
                                      ('/edit_podcast', EditPodcast),
                                      ('/rpc', RPCHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
  
  