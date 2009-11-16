class User(db.Model):
    user = db.UserProperty()
    karma = db.IntegerProperty()
    joined = db.DateTimeProperty()
    