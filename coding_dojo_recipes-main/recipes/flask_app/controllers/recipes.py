from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': session['user_id']}
    return render_template('dashboard.html', user = User.get_user_by_id(data), recipes = Recipe.get_all_recipes())

@app.route('/recipes/<id>')
def view_recipe(id):
    data = {'id': id}
    recipe = Recipe.get_recipe_by_id(data)
    recipe['description'] = recipe['description'].replace("\r\n", "<br>")
    recipe['instructions'] = recipe['instructions'].replace("\r\n", "<br>")
    return render_template('view_recipe.html', recipe = recipe)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/add', methods=['POST'])
def create_recipe():
    data = {
        'creator_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30']
    }
    print(data)
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')
    Recipe.add_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/edit/<id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    return render_template('edit_recipe.html', recipe = Recipe.get_recipe_by_id(data))

@app.route('/recipes/edit', methods=['POST'])
def change_recipe():
    id = request.form['id']
    data = {
        'id': request.form['id'],
        'creator_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30']
    }
    print(data)
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/edit/' + id)
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<id>')
def remove_recipe(id):
    data = {'id': id}
    deleted = Recipe.delete_recipe(data)
    if deleted:
        return redirect('/dashboard')
    else:
        return redirect('/logout')