import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


class Tag(db.Model):
    name = db.StringProperty()


class Post(db.Model):
    content = db.StringProperty(multiline=True)
    #parentPost = db.SelfReferenceProperty()
    parentPost = db.IntegerProperty()
    votes = db.IntegerProperty()
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    tags = db.ReferenceProperty(Tag,collection_name = "tags")



class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    posts = db.GqlQuery("SELECT * FROM Post WHERE parentPost=null ORDER BY date DESC")

    for post in posts:
      if post.author:
        self.response.out.write('<b>%s</b> posted:' % post.author.nickname())
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(post.content))
      self.response.out.write("""
          <form action="/reply" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea><input type="hidden" name="post-key" value="%s" /></div>
            <div><input type="submit" value="Reply!"></div>
          </form>
        </body>
      </html>""" % post.key().id())
      

    # Write the submission form and the footer of the page
    self.response.out.write("""
          <form action="/post" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Post a Question"></div>
          </form>
        </body>
      </html>""")

class PostOverflow(webapp.RequestHandler):
  def post(self):
    post = Post()

    if users.get_current_user():
        post.author = users.get_current_user()

    post.content = self.request.get('content')
    post.put()
    self.redirect('/')

class Reply(webapp.RequestHandler):
    def post(self):
        post = Post()

        if users.get_current_user():
            post.author = users.get_current_user()
        post.content = self.request.get('content')
        post.parentPost = int(self.request.get('post-key'))
        
        post.put()
        self.redirect('/')
        
            
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/post', PostOverflow),
                                      ('/reply', Reply)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()