import app.scripts.pillow as pil
import os
from app import app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, url_for, send_from_directory, flash, session, redirect, jsonify
from dbconnect import connection
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import simplejson

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('root'))

    return wrap
# ---------------------
@app.route('/')
def root():
    return app.send_static_file('pages/mainPage/views/index.html')

@app.route('/login', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = (%s)",[(request.form['username'])])
            
            data = c.fetchone()[2]
            
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("main"))

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error = e)  

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('root'))
		

@app.route('/main', methods=['GET', 'POST'])
def main():
    target = os.path.join(APP_ROOT, '../images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
        print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    return render_template('main.html', user=session['username'])

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('app/images')
    return render_template("gallery.html", image_names=image_names)

@app.route('/bw')
def blacknwhite():
    bw = request.args.get('bw', 0)
    pil.convertb(str('../images/'+bw))
    return jsonify(result='Black and White')

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

@app.route('/register', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()
            x = c.execute("SELECT * FROM users WHERE username = (%s)",[(thwart(username))])
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                          (thwart(userrname), thwart(password)))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('main'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
