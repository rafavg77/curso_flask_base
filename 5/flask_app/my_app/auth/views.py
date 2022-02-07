from flask import Blueprint, session, render_template, abort, request, redirect, url_for, flash, get_flashed_messages

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db

user = Blueprint('auth',__name__)

@user.route('/register', methods=['GET','POST'])
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

@user.route('/login', methods=['GET','POST'])
def login():
   form = LoginForm(meta={'csrf':False})
   
   if form.validate_on_submit():

      user = User.query.filter_by(username = form.username.data).first()
      if user and user.check_password(form.password.data):
         #Registrar Sesion
         session['username'] = user.username
         session['rol'] = user.rol.value
         session['id'] = user.id
         flash('Bienvenido de Nuevo' + user.username)
         return redirect(url_for('product.index'))
      else:
         flash('Credenciales invalidas','danger')
         return redirect(url_for('auth.login'))
      
   if form.errors:
      flash(form.errors,'danger')

   return render_template('auth/login.html', form = form)

@user.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('id', None)
   session.pop('rol', None)
   return redirect(url_for('auth.login'))