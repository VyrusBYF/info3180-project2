from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER =  './app/static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qzihagwqlqcftd:c194ad07a9977b3c675572e557eb3271d3d57a51ac437f2bd5908791fb65f31f@ec2-34-232-147-86.compute-1.amazonaws.com:5432/d3sij232hjde7l" #"postgresql://user:password@localhost/database" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
