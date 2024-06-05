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


connectioni = sqlite3.connect('ingredients.db')
curi = connectioni.cursor()

with open ('ingredients.sql') as fi:
    connectioni.executescript(fi.read())

with open ('../ingredients.csv', 'r') as fi:
    dr = csv.DictReader(fi)
    to_dbi = [(i['i_id'], i['name']) for i in dr]

curi.executemany("INSERT INTO ingredients(i_id, name) VALUES (?, ?);", to_dbi)

connectioni.commit()
connectioni.close()


connectiona = sqlite3.connect('appliances.db')
cura = connectiona.cursor()

with open ('appliances.sql') as fa:
    connectiona.executescript(fa.read())

with open ('../appliances.csv', 'r') as fa:
    dr = csv.DictReader(fa)
    to_dba = [(i['a_id'], i['name']) for i in dr]

cura.executemany("INSERT INTO appliances(a_id, name) VALUES (?, ?);", to_dba)

connectiona.commit()
connectiona.close()