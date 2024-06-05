import sqlite3
import re
from flask import Flask, render_template, request
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_dbi_connection():
    conn = sqlite3.connect('ingredients.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_dba_connection():
    conn = sqlite3.connect('appliances.db')
    conn.row_factory = sqlite3.Row
    return conn

def makelists(recipe):
    if 'ingredients' in recipe:
        recipe['ingredients'] = recipe['ingredients'].split('/')
    
    if 'appliances' in recipe:
        recipe['appliances'] = recipe['appliances'].split('/')

    return recipe


def get_recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE r_id = ?',
                        (recipe_id,)).fetchone()
    conn.close()
    if recipe is None:
        abort(404)
    
    recipe = dict(recipe)
    recipe = makelists(recipe)

    return(recipe)  


app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    conni = get_dbi_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    ingredients = conni.execute('SELECT * FROM ingredients').fetchall()
    conn.close()
    conni.close()

    recipes = [dict(recipe) for recipe in recipes]
    recipes = [makelists(recipe) for recipe in recipes]

    return render_template('index.html', recipes=recipes, ingredients=ingredients )

@app.route('/<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dbinfo')
def dbinfo():
    return render_template('dbinfo.html')

@app.route('/search_results')
def search():
    search_term = request.args.get('search')
    """ Insert regex here instead of LIKE """
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes WHERE name LIKE ?', ('%' + search_term + '%',)).fetchall()

    conn.close()

    recipes = [dict(recipe) for recipe in recipes]
    recipes = [makelists(recipe) for recipe in recipes]

    return render_template('search_results.html', recipes=recipes, search_term=search_term)
