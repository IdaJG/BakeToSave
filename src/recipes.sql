DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
    r_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    time TIME NOT NULL,
    source TEXT NOT NULL,
    link TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    appliances TEXT NOT NULL
);