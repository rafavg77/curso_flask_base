import json
from flask import request
from flask.views import MethodView
from my_app.product.model.category import Category
from my_app.rest_api.helper.request import sendResponseJson
from my_app import app, db

class CategoryAPI(MethodView):
    def get(self, id=None):
        categories = Category.query.all()

        if id:
            category = Category.query.get(id)
            res = CategoryToJson(category)
        else:
            res = []
            for category in categories:
                res.append(CategoryToJson(category))
    
        return sendResponseJson(res,None,200)

    def post(self):
        if not request.form:
            return sendResponseJson(None,"Sin parametro",403)
        
        #validación Nombre
        if not 'name' in request.form:
            return sendResponseJson(None,"Sin parametros name",403)
        
        if len(request.form['name']) < 3:
            return sendResponseJson(None,"Nombre no valido",403)
        
        #validación Precio
        if not 'price' in request.form:
            return sendResponseJson(None,"Sin parametros price",403)
        
        try:
            price = float(request.form['price'])
        except ValueError:
            return sendResponseJson(None,"Precio no valido",403)
        
        #validación categoria
        if not 'category_id' in request.form:
            return sendResponseJson(None,"Sin parametros categoria",403)
        
        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResponseJson(None,"Categoria no valida",403)

        p = Category(request.form['name'],request.form['price'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()

        return sendResponseJson(CategoryToJson(p),None,200)

    def put(self, id):
        categoty = Category.query.get(id)
        if not categoty:
            return sendResponseJson(None,"Categoría No existe",403)
        
        if not request.form:
            return sendResponseJson(None,"Sin parametro",403)
        
        #validación Nombre
        if not 'name' in request.form:
            return sendResponseJson(None,"Sin parametros name",403)
        
        if len(request.form['name']) < 3:
            return sendResponseJson(None,"Nombre no valido",403)
        
        #validación Precio
        if not 'price' in request.form:
            return sendResponseJson(None,"Sin parametros price",403)
        
        try:
            price = float(request.form['price'])
        except ValueError:
            return sendResponseJson(None,"Precio no valido",403)
        
        #validación categoria
        if not 'category_id' in request.form:
            return sendResponseJson(None,"Sin parametros categoria",403)
        
        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResponseJson(None,"Categoria no valida",403)

        categoty.name = request.form['name']
        categoty.price = request.form['price']
        categoty.category_id = request.form['category_id']
        
        db.session.add(categoty)
        db.session.commit()

        return sendResponseJson(CategoryToJson(categoty),None,200)

        return

    def delete(self, id):
        categoty = Category.query.get(id)
        if not categoty:
            return sendResponseJson(None,"Categoría No existe",403)
        
        db.session.delete(categoty)
        db.session.commit()
    
        return sendResponseJson("Categoría eliminado",None,200)

def CategoryToJson(category: Category):
    return {
                'id' : category.id,
                'name' : category.name,
            }
    
category_view = CategoryAPI.as_view('category_view')
app.add_url_rule('/api/categories/',view_func = category_view, methods=['GET','POST'])
app.add_url_rule('/api/categories/<int:id>',view_func = category_view, methods=['GET','PUT','DELETE'])