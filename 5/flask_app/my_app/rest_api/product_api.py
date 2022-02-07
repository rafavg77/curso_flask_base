import json
from unicodedata import category
from flask import jsonify, request
from flask.views import MethodView
from my_app.product.model.product import Product
from my_app.rest_api.helper.request import sendResponseJson
from my_app import app, db

class ProductAPI(MethodView):
    def get(self, id=None):
        products = Product.query.all()

        if id:
            product = Product.query.get(id)
            res = ProductToJson(product)
        else:
            res = []
            for product in products:
                res.append(ProductToJson(product))
    
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

        p = Product(request.form['name'],request.form['price'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()

        return sendResponseJson(ProductToJson(p),None,200)

    def put(self, id):
        product = Product.query.get(id)
        if not product:
            return sendResponseJson(None,"Producto No existe",403)
        
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

        product.name = request.form['name']
        product.price = request.form['price']
        product.category_id = request.form['category_id']
        
        db.session.add(product)
        db.session.commit()

        return sendResponseJson(ProductToJson(product),None,200)

        return

    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            return sendResponseJson(None,"Producto No existe",403)
        
        db.session.delete(product)
        db.session.commit()
    
        return sendResponseJson("Producto eliminado",None,200)

def ProductToJson(product: Product):
    return {
                'id' : product.id,
                'name' : product.name,
                'category_id' : product.category.id,
                'category' : product.category.name
            }
    
product_view = ProductAPI.as_view('product_view')
app.add_url_rule('/api/products/',view_func = product_view, methods=['GET','POST'])
app.add_url_rule('/api/products/<int:id>',view_func = product_view, methods=['GET','PUT','DELETE'])