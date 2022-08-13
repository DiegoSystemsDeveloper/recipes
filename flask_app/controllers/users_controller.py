from flask_app import app
from flask_bcrypt import Bcrypt
from flask import redirect, render_template, request, flash, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

bcript = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')

    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    recipes = Recipe.get_all()
    return render_template('dashboard.html', user = user, recipes=recipes)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    if not User.user_validate_sign_in(request.form):
        return redirect('/')

    user = User.get_by_email(request.form)
    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')
    if not bcript.check_password_hash(user.password, request.form['password']):
        flash('El password es incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    if not User.user_validate_sign_up(request.form):
        return redirect('/')
    pwd = bcript.generate_password_hash(request.form['password'])
    form = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pwd
    }
    id = User.save(form)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

