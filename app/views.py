# pylint: disable=W0311
# pylint: disable=W0312
# pylint: disable=C0111
# pylint: disable=W0611
# pylint: disable=W0612
# pylint: disable=W0613
# pylint: disable=C0303 
# pylint: disable=E1101
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0326
# pylint: disable=R0903
# pylint: disable=R0911
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
import os, json, jwt
from app import app,db
from app.forms import PostForm, RegistrationForm, LoginForm
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, g
from werkzeug.utils import secure_filename
from datetime import date
from app.models import Users, Posts, Likes, Follows
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401
        
        token = parts[1]
        try:
            payload = jwt.decode(token, 'secret')
        except jwt.ExpiredSignature:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401
        g.current_user = user = payload
        #print(g.current_user)
        return f(*args, **kwargs)
    return decorated 








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
        #print(password)
        #print(hashpassword)
        #print(check_password_hash(hashpassword,password))
        #print(hashpassword)
        db.session.add(Users(username=usrname, password=hashpassword, first_name=fname, last_name=lname, email=email, location=location, biography=bio, pro_pic=filename, date_joined=join_date))
        db.session.commit()

        userid = Users.query.with_entities(Users.id).filter_by(username=usrname).first()
        #print(userid[0])
        success_msg= usrname + "registered successfully"
        js_msg = {"message":success_msg, "Username": usrname, "user_id": userid[0], "status":"logged_in"}
        message = jsonify(js_msg)
        #print(message)
        return message
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
                success_msg= usrname + " logged in successfully"
                token = jwt.encode({"user_id": usr.id}, 'secret',algorithm='HS256').decode('utf-8')
                js_msg = {"message":success_msg, "Username": usr.username, "user_id": usr.id, "status": True ,'token': token } 
                message = jsonify(js_msg)
                return message
    return render_template('login.html', error=error)


@app.route('/api/auth/logout', methods=['GET'])
@requires_auth
def logout():
    success_msg=" logged out successfully"
    return jsonify(success_msg)
"""
@app.route('/api/users/<user_id>/posts', methods=['GET','POST'])
def userPosts(user_id):
    form = PostForm()
"""


@app.route('/api/users/<user_id>/posts', methods=['GET','POST'])
@requires_auth
def userPosts(user_id):
    form = PostForm()

    if request.method == 'POST':

        caption = form.caption.data
        created_on = date.today().strftime("%d %b, %Y")
        file = form.photo.data
        #print(user_id);

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('You have registered successfully!', 'success')
        db.session.add(Posts(user_id = user_id, photo = filename, caption = caption, created_on = created_on))
        db.session.commit()

        success_msg = str(user_id) + " You successfully uploaded your post!"
        return jsonify(success_msg)

    elif request.method == 'GET':
        user = Users.query.with_entities(Users.id, Users.first_name, Users.last_name, Users.pro_pic, Users.location, Users.biography, Users.date_joined).filter_by(id = user_id).first()
        info = Posts.query.with_entities(Posts.photo).filter_by(user_id = user_id).order_by(Posts.id.desc()).all()
        post_count = Posts.query.filter_by(user_id = user_id).count()
        follow_count = Follows.query.filter_by(user_id = user_id).count()
        #print(str(g.current_user['user_id']) != str(user_id))
        #print(str(g.current_user['user_id']))
        #print(str(user_id))
        if str(g.current_user['user_id']) != str(user_id):
            followed=Follows.query.filter_by(user_id=user_id,follower_id=g.current_user['user_id']).count()
        else:
        	followed = 3
        details={}
        photos={'pics':[]}
        details['fname']=user[1]
        details['lname']=user[2]
        details['pro_pic']="../static/uploads/" + str(user[3])
        details['location']= user[4]
        details['bio']=user[5]
        details['join_date']= "Member since " + str(user[6])
        details['followed']= followed
        details['user_id']= user_id

        for pic in info:
            photos['pics'].append("../static/uploads/" + str(pic[0]))
        return jsonify(user = details, posts = post_count, followers=follow_count, photos = photos)
    return jsonify('Something went wrong!')


@app.route('/api/posts', methods=['GET'])
@requires_auth
def posts():
    posts=[]
    results=Posts.query.with_entities(Users.username, Users.pro_pic, Posts.photo, Posts.caption, Posts.created_on, Posts.id, Posts.user_id).join(Users, Users.id == Posts.user_id).order_by(Posts.id.desc()).all()
    #results = Posts.query.with_entities(Posts.user_id,Posts.photo, Posts.caption,Posts.created_on).all()
    for post in results:
       	lcount=Likes.query.filter_by(post_id=post[5]).count()
       	liked=Likes.query.filter_by(post_id=post[5],user_id=g.current_user['user_id']).count()
       	#print (lcount)
       	temp={}
       	temp['username'] = post[0]
       	temp['propic']   = "../static/uploads/" + str(post[1])
       	temp['photo']    = "../static/uploads/" + str(post[2])
       	temp['caption']  = post[3]
       	temp['created']  = post[4]
       	temp['likes']    = lcount
       	temp['post_id']  = post[5]
       	temp['liked']    = liked
       	temp['post_uid'] = post[6]
       	posts.append(temp)
    users=Posts.query.with_entities(Users.id).all()
    return jsonify(posts = posts, users = users) 

@app.route('/api/users/<user_id>/follow', methods=['POST'])
@requires_auth
def follow(user_id):
	if request.method == 'POST':
		followed=Follows.query.filter_by(user_id=user_id,follower_id=g.current_user['user_id']).count()
		if followed == 0:
			db.session.add(Follows(user_id=user_id,follower_id=g.current_user['user_id']))
			db.session.commit()
			followed=Follows.query.filter_by(user_id=user_id,follower_id=g.current_user['user_id']).count()
			#print(followed)
			success_msg=1
		else:
			Follows.query.filter_by(user_id=user_id,follower_id=g.current_user['user_id']).delete()
			db.session.commit()
			followed=Follows.query.filter_by(user_id=user_id,follower_id=g.current_user['user_id']).count()
			#print(followed)
			success_msg=0
		return jsonify(success_msg)


@app.route('/api/posts/<post_id>/like', methods=['POST'])
@requires_auth
def like(post_id):
	if request.method == 'POST':
		liked=Likes.query.filter_by(post_id=post_id,user_id=g.current_user['user_id']).count()
		if liked == 0:
			db.session.add(Likes(post_id=post_id,user_id=g.current_user['user_id']))
			db.session.commit()
			liked=Likes.query.filter_by(post_id=post_id,user_id=g.current_user['user_id']).count()
			#print(liked)
			success_msg=1
		else:
			Likes.query.filter_by(post_id=post_id,user_id=g.current_user['user_id']).delete()
			db.session.commit()
			liked=Likes.query.filter_by(post_id=post_id,user_id=g.current_user['user_id']).count()
			#print(liked)
			success_msg=0
		return jsonify(success_msg)





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
