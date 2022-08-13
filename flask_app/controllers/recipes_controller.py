from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/new/recipe')
def new_recipe():
    if not 'user_id' in  session:
        return redirect('/')
    user = session['user_id']
    return render_template('new_recipe.html', user=user)

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if not 'user_id' in  session:
        return redirect('/')
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if not 'user_id' in  session:
        return redirect('/')
    recipe = Recipe.get_by_id({'id': id})
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    if not 'user_id' in  session:
        return redirect('/')
    if not Recipe.validate_join_recipe({'id': id, 'user_id': session['user_id']}):
        return redirect('/error')
    if not Recipe.valida_receta(request.form):
        return redirect(f'/edit/recipe/{request.form["id"]}')
    Recipe.update_recipe(request.form)
    return redirect('/dashboard')

@app.route('/show/recipe/<int:id>')
def show_recipe(id):
    if not 'user_id' in  session:
        return redirect('/')
    recipe = Recipe.get_by_id({'id': id})
    user = User.get_by_id({'id': session['user_id']})
    return render_template('show_recipe.html', user=user, recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if not 'user_id' in  session:
        return redirect('/')
    if not Recipe.validate_join_recipe({'id': id, 'user_id': session['user_id']}):
        return redirect('/error')
    Recipe.delete_recipe({'id': id})
    return redirect('/dashboard')

@app.route('/error')
def error():
    session.clear()
    return render_template('error.html')
    
    
    