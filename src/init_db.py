import csv, sqlite3

connection = sqlite3.connect('recipes.db')
cur = connection.cursor()

with open ('recipes.sql') as f:
    connection.executescript(f.read())

with open ('../recipes.csv', 'r') as f:
    dr = csv.DictReader(f)
    to_db = [(i['r_id'], i['name'], i['category'], i['time'], i['source'], i['link'], i['ingredients'], i['appliances']) for i in dr]

cur.executemany("INSERT INTO recipes(r_id, name, category, time, source, link, ingredients, appliances) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)

connection.commit()
connection.close()