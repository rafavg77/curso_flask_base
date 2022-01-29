#from my_app import app
from crypt import methods
from os import abort
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages
from my_app import db
from my_app.product.model.products import PRODUCTS
from my_app.product.model.product import Product, ProductForm
from my_app.product.model.product import ProductForm
from sqlalchemy.sql.expression import not_, or_

product = Blueprint('product',__name__)

@product.route('/product')
@product.route('/product/<int:page>')
def index(page=1):
   return render_template('product/index.html',products=Product.query.paginate(page,5))

@product.route('/product/<int:id>')
def show(id):
   product = Product.query.get_or_404(id)
   #if not product:
   #   abort(404)
   return render_template('product/show.html', product=product)

@product.route('/test')
def test():
   #p = Product.query.limit(2).first()
   #p = Product.query.order_by(Product.id).limit(2).first()
   #p = Product.query.order_by(Product.id).limit(2).all()
   #p = Product.query.order_by(Product.id.desc()).all()
   #p = Product.query.get({"id":1})
   #p = Product.query.filter_by(name = "iPhone").all()
   #p = Product.query.filter(Product.id > 1).all()
   #p = Product.query.filter_by(name = "iPhone", id=2).all()
   #p = Product.query.filter(Product.name.like('M%')).all()
   #p = Product.query.filter(not_(Product.id > 1)).all()
   #p = Product.query.filter(or_(Product.id > 1, Product.name=="iPhone")).all()
   #print(p)

   #Insertar
   # p = Product("Xiaomi","500")
   # db.session.add(p)
   # db.session.commit()

   #Actualizar
   # p = Product.query.filter_by(id=1).first()
   # print(p)
   # p.name = "iPhone 12"
   # db.session.add(p)
   # db.session.commit()

   #Eliminar
   # p = Product.query.filter_by(id=9).first()
   # db.session.delete(p)
   # db.session.commit()

   return "Flask"

@product.route('/filter/<int:id>')
def filter(id):
   product = PRODUCTS.get(id)
   return render_template('product/filter.html',product=product)

@product.route('/product-create', methods=['GET','POST'])
def create():
   form = ProductForm(meta={'csrf':False})
   if form.validate_on_submit():
      p = Product(request.form['name'],request.form['price'])
      db.session.add(p)
      db.session.commit()
      flash('Producto creado con exito')
      return redirect(url_for('product.create'))
   
   if form.errors:
      flash(form.errors,'danger')

   return render_template('product/create.html', form = form)

@product.route('/product-update/<int:id>',methods=['GET','POST'])
def update(id):
   product = Product.query.get_or_404(id)
   form = ProductForm(meta={'csrf':False})

   if request.method == 'GET':
      form.name.data = product.name
      form.price.data = product.price
   
   if form.validate_on_submit():
      #Actualziar Producto
      product.name = form.name.data
      product.price = form.price.data

      db.session.add(product)
      db.session.commit()

      flash('Producto Actualziado con Éxito')
      return redirect(url_for('product.update',id=product.id))
   
   if form.errors:
      flash(form.errors,'danger')
   
   return render_template('product/update.html',product=product,form=form)

@product.route('/product-delete/<int:id>')
def delete(id):
   product = Product.query.get_or_404(id)
   db.session.delete(product)
   db.session.commit()
   flash('Producto Eliminado con Éxito')

   return redirect(url_for('product.index'))


@product.app_template_filter('iva')
def reverse_filter(product):
   if product['price']:
      return product['price'] * .20 + product['price']
   return "Sin Precio"

