from google.appengine.ext import db

class Podcast(db.Model):
    owner = db.UserProperty()
    create_date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    
class PodcastItem(db.Model):
    podcast = db.ReferenceProperty(Podcast)
    title = db.StringProperty()
    uri = db.StringProperty()
