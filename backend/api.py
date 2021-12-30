import flask
from flask import Flask, jsonify, request
from pathlib import Path

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


@app.route("/meals/create", methods=["POST"])
def create_meal() -> str:
    """Create a meal and commit it to DB.

    Returns:
        str: String saying that everything went OK.
    """
    
    path = Path(__file__).parent / "assets"
    
    image = request.files["image"]
    
    if image.filename != "":
        image.save(f"{path}/{image.filename}")
    
    query = f"INSERT INTO meal (meal_name, meal_image) VALUES ('{request.form['name']}', '{image.filename}')"
    
    mycursor.execute(query)
    
    mydb.commit()
    
    return "OK"
    


app.run(host="0.0.0.0")
