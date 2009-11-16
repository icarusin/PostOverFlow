class Tag(db.Model):
    name = db.StringProperty()
    posts = db.ListProperty()
    