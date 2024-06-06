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
    conna = get_dba_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    ingredients = conni.execute('SELECT * FROM ingredients').fetchall()
    appliances = conna.execute('SELECT * FROM appliances').fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM recipes').fetchall()
    conn.close()
    conni.close()
    conna.close()

    recipes = [dict(recipe) for recipe in recipes]
    recipes = [makelists(recipe) for recipe in recipes]

    return render_template('index.html', recipes=recipes, ingredients=ingredients, appliances=appliances, 
                           categories=[category['category'] for category in categories])

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

    if not search_term:
        return render_template('search_results.html', recipes=[], search_term=search_term)
    normalized_search_term = search_term.replace('å', 'aa').replace('ø', 'oe').replace('æ','ae')
    terms = normalized_search_term.split()
    patterns = [re.compile(re.escape(term), re.IGNORECASE) for term in terms]

    conn = get_db_connection()
    conni = get_dbi_connection()
    conna = get_dba_connection()

    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    ingredients = conni.execute('SELECT * FROM ingredients').fetchall()
    appliances = conna.execute('SELECT * FROM appliances').fetchall()

    conn.close()
    conni.close()
    conna.close()

    recipes = [dict(recipe) for recipe in recipes]
    recipes = [makelists(recipe) for recipe in recipes]

    matching_recipes = []
    for recipe in recipes:
        try:
            if all(pattern.search(recipe['name']) for pattern in patterns):
                matching_recipes.append(recipe)
        except re.error as e:
            # Handle potential regex errors gracefully
            print(f"Regex error: {e}")

    return render_template('search_results.html', recipes=matching_recipes, search_term=search_term, 
                           ingredients=ingredients, appliances=appliances)

@app.route('/tick_results')
def tick():
    ticked_ingredients = request.args.getlist('ingredients')
    ticked_appliances = request.args.getlist('appliances')
    ticked_categories = request.args.getlist('categories')

    ingredient_query_string = " AND ".join(["ingredients LIKE ?"] * len(ticked_ingredients))
    appliance_query_string = " AND ".join(["appliances NOT LIKE ?"] * len(ticked_appliances))
    category_query_string = " OR ".join(["category = ?"] * len(ticked_categories))

    combined_query_string = ""
    query_params = []

    if ticked_ingredients:
        combined_query_string += ingredient_query_string
        query_params.extend(['%' + ingredient + '%' for ingredient in ticked_ingredients])

    if ticked_appliances:
        if combined_query_string:
            combined_query_string += " AND "
        combined_query_string += appliance_query_string
        query_params.extend(['%' + appliance + '%' for appliance in ticked_appliances])

    if ticked_categories:
        if combined_query_string:
            combined_query_string += " AND ("
        combined_query_string += category_query_string
        if ticked_ingredients or ticked_appliances:
            combined_query_string += ")"
        query_params.extend(ticked_categories)

    conn = get_db_connection()
    conni = get_dbi_connection()
    conna = get_dba_connection()

    if combined_query_string:
        recipes = conn.execute(f'SELECT * FROM recipes WHERE {combined_query_string}', query_params).fetchall()
    else:
        recipes = conn.execute('SELECT * FROM recipes').fetchall()

    ingredients = conni.execute('SELECT * FROM ingredients').fetchall()
    appliances = conna.execute('SELECT * FROM appliances').fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM recipes').fetchall()

    conn.close()
    conni.close()
    conna.close()

    recipes = [dict(recipe) for recipe in recipes]
    recipes = [makelists(recipe) for recipe in recipes]

    return render_template('tick_results.html', recipes=recipes, 
                           ticked_ingredients=ticked_ingredients, ticked_appliances=ticked_appliances, ticked_categories=ticked_categories, 
                           ingredients=ingredients, appliances=appliances, categories=[category['category'] for category in categories])
