from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER =  './app/static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bdtxsbuhtowhtd:3eedd4dd6e059466dc83a836e39318d99e2ce2e48a38bbb72fe860d940533f3b@ec2-34-202-88-122.compute-1.amazonaws.com:5432/d255nu1mk26ugo' #"postgresql://user:password@localhost/database" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
