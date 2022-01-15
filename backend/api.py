import flask
from flask import Flask, jsonify, request, send_from_directory, abort
from pathlib import Path
from os.path import isfile

from db import mydb, mycursor

# Defining app and config
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def home() -> str:
    """Home route. Can be used to check if the API is up and running.

    Returns:
        str: Returns that API is up and running.
    """
    
    return "API is up and running!"


@app.route("/meals", methods=["GET"])
def get_meals() -> flask.wrappers.Response:
    """Get all meals from DB.

    Returns:
        flask.wrappers.Response: Jsonified response.
    """
    
    query = "SELECT * FROM meal"
    
    mycursor.execute(query)
    
    myres = mycursor.fetchall()
    
    print(type(jsonify(myres)))
    
    return jsonify(myres)


@app.route("/ingredients/<int:meal_id>", methods=["GET"])
def get_meal_ingredients(meal_id: int) -> flask.wrappers.Response:
    """Get ingredients of specific meal from DB.

    Args:
        meal_id (int): Meal ID

    Returns:
        flask.wrappers.Response: Jsonified response.
    """
    
    query = f"SELECT * FROM ingredients WHERE meal_id={meal_id}"
    
    mycursor.execute(query)
    
    myres = mycursor.fetchall()
    
    return jsonify(myres)


@app.route("/ingredients/add", methods=["POST"])
def add_ingredient():
    
    data = request.form.to_dict()
    
    query = f"SELECT id FROM ingredients WHERE ingredient_name='{data['ingredient_name']}' AND unit='{data['unit']}'"
    
    mycursor.execute(query)
    
    myres = mycursor.fetchall()
    
    if len(myres) > 0:
        abort(409)
    
    query = f"INSERT INTO ingredients (\
        ingredient_name,\
        unit,\
        cost_per_unit,\
        calories_per_unit,\
        protein_per_unit,\
        carbs_per_unit,\
        fat_per_unit)\
        VALUES ('{data['ingredient_name']}',\
            '{data['unit']}',\
            '{data['cost_per_unit']}',\
            '{data['calories_per_unit']}',\
            '{data['protein_per_unit']}',\
            '{data['carbs_per_unit']}',\
            '{data['fat_per_unit']}')"
        
    mycursor.execute(query)
    
    mydb.commit()
    
    return "", 200


@app.route("/meals/create", methods=["POST"])
def create_meal() -> str:
    """Create a meal and commit it to DB.

    Returns:
        str: String saying that everything went OK.
    """
    
    path = Path(__file__).parent / "assets"
    
    image = request.files["image"]
    
    if image.filename != "" and not isfile(f"{path}/{image.filename}"):
        image.save(f"{path}/{image.filename}")
    
    query = f"SELECT meal_name FROM meal WHERE meal_name='{request.form['name']}'"
    
    mycursor.execute(query)
    
    myres = mycursor.fetchall()
    
    # Returns a duplicate error
    if len(myres) > 0:
        abort(409)
    
    query = f"INSERT INTO meal (meal_name, meal_image) VALUES ('{request.form['name']}', '{image.filename}')"
    
    mycursor.execute(query)
    
    mydb.commit()
    
    return "", 200
    
    
@app.route("/images/<path:file>", methods=["GET"])
def get_image(file: str):
    
    path = Path(__file__).parent / "assets"
    
    return send_from_directory(path, file)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")
