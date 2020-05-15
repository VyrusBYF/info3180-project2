from . import db
from werkzeug.security import generate_password_hash

class Users(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(80))
    biography = db.Column(db.String(500))
    pro_pic=db.Column(db.String(300))
    date_joined = db.Column(db.String(30))

    def __init__(self, first_name, last_name, username, password, email, location, biography, date_joined, pro_pic):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.email = email
        self.location = location
        self.biography = biography
        self.date_joined = date_joined
        self.pro_pic = pro_pic
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class Posts (db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, nullable = False)
    photo = db.Column(db.String(300))
    caption = db.Column(db.String(500))
    created_on = db.Column(db.String(30))


class Likes (db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, nullable = False)
    post_id = db.Column(db.Integer)



class Follows (db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, nullable = False)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, nullable = False)