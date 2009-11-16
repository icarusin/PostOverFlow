class Post(db.Model):
    replies = db.ListProperty(Post)
    votes = db.IntegerProperty()
    author = db.UserProperty()
    date = db.DateTimeProperty()
    tags = db.ListProperty()