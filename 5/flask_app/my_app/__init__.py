from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps

app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "fauth.login"

def rol_admin_need(f):
   @wraps(f)
   def wrapper(*args, **kwds):
      if current_user.rol.value != "admin":
         #return "Tu debes ser admin",403
         #print('Calling decorated function ' + str(current_user.rol.value))
         logout_user()
         login_manager.unauthorized()
         return redirect(url_for('fauth.login'))
      return f(*args, **kwds)
   return wrapper

from my_app.product.product import product
from my_app.product.category import category
from my_app.auth.views import user
from my_app.futh.fauthController import fauth

#rest

from my_app.rest_api.product_api import product_view
from my_app.rest_api.category_api import category_view

#Importar las vistas
app.register_blueprint(product)
app.register_blueprint(category)
#app.register_blueprint(user)
app.register_blueprint(fauth)

db.create_all()

@app.template_filter('mydouble')
def reverse_filter(n:float):
   return n*2