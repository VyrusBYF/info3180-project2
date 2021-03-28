from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER =  './app/static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://cyyeesvvwqzmbr:49ea26f5d727d2954a025c25e8d25da6809a5f063d6aff71ba8db19c5d820cc7@ec2-3-211-37-117.compute-1.amazonaws.com:5432/d502pffmd7sg8b" #"postgresql://user:password@localhost/database" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
