#from my_app import app
from crypt import methods
from os import abort
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages

from my_app import db
from my_app.product.model.category import Category, CategoryForm
from sqlalchemy.sql.expression import not_, or_

category = Blueprint('category',__name__)

@category.route('/category')
@category.route('/category/<int:page>')
def index(page=1):
   return render_template('category/index.html',categories=Category.query.paginate(page,5))

@category.route('/show-category/<int:id>')
def show_category(id):
   print(id)
   category = Category.query.get_or_404(id)
   print("category")
   print(category)
   #if not category:
   #   abort(404)
   return render_template('category/show-category.html', category=category)

@category.route('/category-create', methods=['GET','POST'])
def create():
   form = CategoryForm(meta={'csrf':False})
   if form.validate_on_submit():
      p = Category(request.form['name'])
      db.session.add(p)
      db.session.commit()
      flash('Categoria creado con exito')
      return redirect(url_for('category.create'))
   
   if form.errors:
      flash(form.errors,'danger')

   return render_template('category/create.html', form = form)

@category.route('/category-update/<int:id>',methods=['GET','POST'])
def update(id):
   category = Category.query.get_or_404(id)
   form = CategoryForm(meta={'csrf':False})

   print(category.products)

   if request.method == 'GET':
      form.name.data = category.name
   
   if form.validate_on_submit():
      category.name = form.name.data
      db.session.add(category)
      db.session.commit()
      flash('Categoria Actualziado con Éxito')
      return redirect(url_for('category.update',id=category.id))
   
   if form.errors:
      flash(form.errors,'danger')
   
   return render_template('category/update.html',category=category,form=form)

@category.route('/category-delete/<int:id>')
def delete(id):
   category = Category.query.get_or_404(id)
   db.session.delete(category)
   db.session.commit()
   flash('Categoria Eliminado con Éxito')

   return redirect(url_for('category.index'))


@category.app_template_filter('iva')
def reverse_filter(category):
   if category['price']:
      return category['price'] * .20 + category['price']
   return "Sin Precio"

