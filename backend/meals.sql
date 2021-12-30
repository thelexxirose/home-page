DROP TABLE meal;
DROP TABLE ingredients;

CREATE TABLE meal (
    id int NOT NULL AUTO_INCREMENT,
    meal_name varchar(255),
    meal_image varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE ingredients (
    id int NOT NULL AUTO_INCREMENT,
    meal_id int NOT NULL,
    ingredient_name varchar(255),
    amount float(2),
    unit varchar(255),
    cost_per_unit float(2),
    calories_per_unit float(2),
    protein_per_unit float(2),
    carbs_per_unit float(2),
    fat_per_unit float(2),
    PRIMARY KEY (id)
);