import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    template_path =  os.path.join(os.path.dirname(__file__), 'templates')
    def get(self):
        user = users.get_current_user()
        if user:
            path = os.path.join(self.template_path, 'main.html')
            template_values = {
                'user' : user
            }
            self.response.out.write(template.render(path, template_values))
            
        else:
            self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
  
  