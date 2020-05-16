# pylint: disable=W0312
# pylint: disable=C0111
# pylint: disable=W0611
# pylint: disable=C0303 
# pylint: disable=E1101
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0326
# pylint: disable=R0903
# pylint: disable=R0912
# pylint: disable=C0411
# pylint: disable=C0412
# pylint: disable=C0121



"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app,db
from app.forms import PostForm, RegistrationForm, LoginForm
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from datetime import date
from app.models import Users, Posts, Likes, Follows
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".

    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")




@app.route('/api/users/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        usrname = form.username.data
        password = form.password.data
        hashpassword = generate_password_hash(password)
        fname = form.firstname.data
        lname = form.lastname.data
        email = form.email.data
        location = form.location.data
        bio = form.biography.data
        join_date = date.today().strftime("%B %Y")

        file = form.photo.data

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('You have registered successfully!', 'success')
        print(password)
        print(hashpassword)
        print(check_password_hash(hashpassword,password))
        print(hashpassword)
        db.session.add(Users(username=usrname, password=hashpassword, first_name=fname, last_name=lname, email=email, location=location, biography=bio, pro_pic=filename, date_joined=join_date))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html',form = form)

@app.route('/api/auth/login', methods=['POST'])
def login():
    error = None
    login = LoginForm()
    if request.method == 'POST':
        usrname = login.username.data
        passwrd = login.password.data
        usr=Users.query.filter_by(username=usrname).first()
        if usr == None :
            error = 'Invalid username or password'
            print (error)
        else:
            if check_password_hash(usr.password,passwrd) == True:
                print ("Logged IN")

                session['logged_in'] = True   
                flash('You were logged in', 'success')
                return redirect(url_for('posts'))

    return render_template('login.html', error=error)

@app.route('/api/auth/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('index'))

@app.route('/api/users/{user_id}/posts', methods=['GET','POST'])
def userPosts():
     form = RegistrationForm()
    if request.method == 'POST':

        caption = form.biography.data
        created_on = date.today().strftime("%d %b, %Y")
        user_id = user_id
        file = form.photo.data

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('You have registered successfully!', 'success')
        print(password)
        print(hashpassword)
        print(check_password_hash(hashpassword,password))
        print(hashpassword)
        db.session.add(Users(user_id = user_id, photo = filename, caption = caption, created_on = created_on))
        db.session.commit()
        return redirect(url_for('index'))
    
    return 0

@app.route('/api/users/{user_id}/follow', methods=['POST'])
def follow():
    return 0

@app.route('/api/posts', methods=['GET'])
def posts():
    return 0


@app.route('/api/posts/{post_id}/like', methods=['POST'])
def like():
    return 0





#----------------------------------------------------------------------------------------------------------------------------------------------------------






"""


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not session.get('logged_in'):
        abort(401)

    # Instantiate your form class
    if request.method == 'GET':
        Upload = UploadForm()
        return render_template('upload.html', form = Upload)

    # Validate file upload on submit
    Upload = UploadForm()

    if request.method == 'POST':
        # Get file data and save to your uploads folder
        file = Upload.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File Saved', 'success')
        return redirect(url_for('home'))

    return redirect(url_for('home'))

def get_uploaded_images():
    rootdir = os.getcwd()
    print(rootdir)
    lst = []
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            lst.append(file)
        print os.path.join(subdir, file)
    return lst[1:] #The first file is the gitkeep, so we skip it.


@app.route('/files')
def files():
    if not session.get('logged_in'):
         abort(401)
    return render_template('files.html', file = get_uploaded_images())


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    #Send your static text file.
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
"""

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
