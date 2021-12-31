from flask import Flask, render_template
import requests
from pathlib import Path

# Defining app and config
app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def home():
    
    path = Path(__file__).parent.parent / "backend/assets"
    
    meals = requests.get("http://localhost:5000/meals").json()
    
    for i, meal in enumerate(meals):
        meals[i].append(f"http://192.168.38.100:5000/images/{ meal[2] }")
    
    print(meals[2])

    
    return render_template(
        "meals.html",
        meals=meals
    )
    
@app.route("/meal/<int:meal_id>", methods=["GET"])
def meal(meal_id: int):
    return f"Meal ID: {meal_id}"
    
    
app.run(host="0.0.0.0", port=5001)