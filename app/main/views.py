from app import db
from . import main
from flask import request, render_template, redirect, url_for, flash, make_response, session, current_app
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Feedback
from app.utils import send_mail, create_db
from .forms import ContactForm, LoginForm, SignUpForm


@main.route('/')
def index():
    return render_template('index.html', name='Jerry')

@main.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'<h2>Profile page of user #{user_id}</h2>'

@main.route('/books/<genre>')
def books(genre):
    return f'<h4>All books in {genre} category.</h4>'

@main.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User(name=name, username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('User SignUp', 'success')
        return redirect(url_for('.login'))
    return render_template('signup.html', form=form)

@main.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.admin'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('.admin'))

        flash('Invalid username/password', 'error')
        return redirect(url_for('.login'))
    return render_template('login.html', form=form)

@main.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.login'))
    
@main.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        feedback = Feedback(name=name, email=email, message=message)
        db.session.add(feedback)
        db.session.commit()

        msg_body = f'You have recieved a new feedback from {name} <{email}>'

        send_mail('New Feedback', current_app.config['MAIL_DEFAULT_SENDER'], 'mail/feedback.html', name=name, email=email)

        flash('Message Received', 'success')
        return redirect(url_for('.contact'))

    return render_template('contact.html', form=form)

@main.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response('Setting a cookie')
        res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    else:
        res = make_response(f'Value of cookie foo is {request.cookies.get("foo")}')
    return res

@main.route('/delete_cookie/')
def delete_cookie():
    res = make_response('Cookie Removed')
    res.set_cookie('foo', 'bar', max_age=0)
    return res

@main.route('/article/', methods=['GET', 'POST'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response('')
        res.set_cookie('font', request.form.get('font'), 60*60*24*15)
        res.headers['location'] = url_for('.article')
        return res, 302
    return render_template('article.html')

@main.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f'Total visits: {session.get("visits")}'

@main.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)
    return 'Visits delete!'

@main.route('/session/')
def update_session():
    res = str(session.items())

    cart_item = {'pinapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        session['cart_item']['pinapples'] = '100'
        session.modified = True
    else:
        session['cart_item'] = cart_item
    return res

@main.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@main.route('/db-create/')
def db_create():
    create_db()
