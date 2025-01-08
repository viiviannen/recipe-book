from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm, RecipeForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Recipe
from app.email import send_password_reset_email
from urllib.parse import urlsplit
from jinja2 import pass_context
from markupsafe import Markup, escape
import re

# Custom nl2br filter
@app.template_filter('nl2br')
def nl2br(value):
    # Convert newlines in text to <br> tags for HTML rendering
    _newline_re = re.compile(r'(?:\r\n|\r|\n)+')
    result = u'<br>'.join(escape(line) for line in _newline_re.split(value))
    return Markup(result)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    #print(f"Current user: {current_user}, ID: {current_user.id}")
    form = RecipeForm(mode="add")
    if form.validate_on_submit():
        #print(f"Form submitted, Recipe Name: {form.name.data}, Ingredients: {form.ingredients.data}, Instructions: {form.instructions.data}")
        #print(f"Current user during form submit: {current_user}, ID: {current_user.id}")
        
        recipe = Recipe(
            name=form.name.data, 
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
            )
        #print(f"Recipe to be added: {recipe}, User ID: {recipe.user_id}")
        
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added!')
        return redirect(url_for('index'))
    
    recipes = db.session.scalars(
        sa.select(Recipe).where(Recipe.user_id == current_user.id)
        .order_by(Recipe.timestamp.desc())
    ).all()
    
    return render_template('index.html', title='Home', form=form, recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    
    return render_template('user.html', user=user)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/recipe/<int:recipe_id>')
@login_required
def recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if recipe is None or recipe.author != current_user:
        flash("Recipe not found or you don't have access to it.")
        return redirect(url_for('index'))
    return render_template('recipe.html', title=recipe.name, recipe=recipe)

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if recipe is None or recipe.author != current_user:
        flash("Recipe not found or you don't have access to it.")
        return redirect(url_for('index'))

    form = RecipeForm(mode="edit", obj=recipe)  # Pre-populate the form with existing data

    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        flash("Recipe updated!")
        return redirect(url_for('recipe', recipe_id=recipe.id))

    # Pass the form and set the editing flag
    return render_template('recipe.html', title=f"Edit {recipe.name}", recipe=recipe, form=form, editing=True)

@app.route('/delete_recipe/<int:recipe_id>', methods=['GET'])
@login_required
def delete_recipe(recipe_id):
    # Find the recipe
    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if the current user is the owner of the recipe
    if recipe.user_id != current_user.id:
        flash('You can only delete your own recipes.', 'warning')
        return redirect(url_for('index'))

    # Delete the recipe
    db.session.delete(recipe)
    db.session.commit()

    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))