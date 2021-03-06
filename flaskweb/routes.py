import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskweb import app, db, bcrypt
from flaskweb.forms import RegistrationForm, LoginForm, UpdateAccountForm, RegisterSickessForm
from flaskweb.models import User, Disease, user_disease, Contact_log
from flask_login import login_user, current_user, logout_user, login_required


posts=[
    {
      'Student':'VAMSI',
	  'title':'Keyboard',
	  'content':'gaming keyboard',
	  'date_posted':'January 12,2020'

     },	
     {
      'Student':'Pretham',
	  'title':'Wallet',
	  'content':'Mens Wallet',
	  'date_posted':'January 20,2020'

     }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/report_sickness", methods=["GET", "POST"])
@login_required
def report_sickness():
    form = RegisterSickessForm()
    if form.validate_on_submit():
        disease = {
            'disease_name': form.disease.data,
            'disease_description':form.disease_description.data 
        }
        savedDisease = Disease(**disease)
        db.session.add(savedDisease)
        db.session.commit()
        
        user = db.session.query(User).filter_by(username = form.contact_name.data).first()
        if not user:
            hashed_password = bcrypt.generate_password_hash(form.contact_name.data).decode('utf-8')
            user = User(username=form.contact_name.data, email=form.contact_name.data+ '@' + form.contact_name.data + '.' + 'com', password=hashed_password)
            db.session.add(user)
            db.session.commit()
            
        contLog = {
            'user_id':user.id,
            "disease_id": savedDisease.disease_id,
            "start_date": form.sicknes_start_date.data,
            "end_date": form.sicknes_end_date.data
        }
        userDisease = user_disease(**contLog)
        db.session.add(userDisease)
        db.session.commit()
        flash("The sickness has be saved!", "success")

        data = db.session.query(User)\
                .join(user_disease, user_disease.user_id == User.id)\
                .join(Disease, Disease.disease_id == user_disease.disease_id)\
                .add_columns(User.id, User.username, Disease.disease_name, user_disease.start_date, user_disease.end_date )\
                .filter(User.id == user_disease.user_id)\
                .all()
        
        return render_template("report_sickness.html", title="Sickness Report", form=form, data=data)
    elif request.method == "GET":
        data = db.session.query(User)\
                .join(user_disease, user_disease.user_id == User.id)\
                .join(Disease, Disease.disease_id == user_disease.disease_id)\
                .add_columns(User.id, User.username, Disease.disease_name, user_disease.start_date, user_disease.end_date )\
                .filter(User.id == user_disease.user_id)\
                .all()

        # print(data)
        list = [ { 
            "id": item.id,
            "username": item.username,
            "disease_name": item.disease_name,
            "start_date": item.start_date,
            "end_date" : item.end_date

        } for item in data ]
        print(list)

        return render_template("report_sickness.html", title='Sickness Report', form=form, posts=list )
