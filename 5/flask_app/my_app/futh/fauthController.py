from flask import Blueprint, session, render_template, abort, request, redirect, url_for, flash, get_flashed_messages

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db
from flask_login import current_user, login_user, logout_user, login_required
from my_app import login_manager

fauth = Blueprint('fauth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@fauth.route('/register', methods=['GET','POST'])
def register():

   if session.get('username'):
      print(session['username'])

   form = RegisterForm(meta={'csrf':False})
   
   if form.validate_on_submit():
      if User.query.filter_by(username = form.username.data).first():
         flash("El usuario ya existe",'danger')
      else:
         p = User(form.username.data, form.password.data)
         db.session.add(p)
         db.session.commit()
         flash('Usuario creado con exito')
         return redirect(url_for('auth.register'))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('auth/register.html', form = form)


@fauth.route('/login', methods=['GET','POST'])
def login():
   if current_user.is_authenticated:
      flash('Ya estás autenticado')
      return redirect(url_for('product.index'))

   form = LoginForm(meta={'csrf':False})
   
   if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Bienvenido de Nuevo ' + user.username)

            next = request.form['next']
            print(next)
            #if not is_safe_url(next):
            #   return abort(404)
            return redirect(next or url_for('product.index'))

            #return redirect(url_for('product.index'))
        else:
            flash('Credenciales invalidas','danger')
            return redirect(url_for('fauth.login'))
      
   if form.errors:
      flash(form.errors,'danger')

   return render_template('auth/login.html', form = form)

@fauth.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('fauth.login'))

@fauth.route('/protegida')
@login_required
def protegida():
   return "Vista Protegida"