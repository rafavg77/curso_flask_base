from flask import Blueprint

hello2 = Blueprint('hello2',__name__)

@hello2.route('/hello1')
def hello1():
   return "Hola mundo 1"