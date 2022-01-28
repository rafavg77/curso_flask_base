#from my_app import app
from flask import Blueprint

hello = Blueprint('hello',__name__)

@hello.route('/d')
@hello.route('/hello')
def fhello():
   return "Hola mundo"