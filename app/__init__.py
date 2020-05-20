from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER =  './app/static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qtvjqgwanzhurf:f8176ebe7a770f9500f9824d4a94f276c08b3c3710135beb80a4f470e4a64a00@ec2-34-200-72-77.compute-1.amazonaws.com:5432/db52od3ufs9krn' #"postgresql://user:password@localhost/database" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
