from flask import Flask, render_template, request, redirect, url_for
import requests

# Defining app and config
app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def home():
    
    #path = Path(__file__).parent.parent / "backend/assets"
    
    meals = requests.get("http://localhost:5000/meals").json()
    
    for i, meal in enumerate(meals):
        meals[i].append(f"https://backend.thelexxirose.tech/images/{ meal[2] }")
    
    print(meals[2])

    
    return render_template(
        "meals.html",
        meals=meals
    )
    
@app.route("/meals/<int:meal_id>", methods=["GET"])
def meal(meal_id: int):
    return render_template(
        "create_meal.html"                
    )
    
@app.route("/meals/create", methods=["GET", "POST"])
def create_meal():
    if request.method == "POST":
        img = request.files["image"]
        
        data = { 
            "name": request.form["title"]
        }
        
        f = {
            "image": (img.filename, img.stream.read(), "multipart/form-data")
        }
        
        requests.post("http://localhost:5000/meals/create", data=data, files=f)
    
    return render_template(
        "create_meal.html"                
    )

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")
  
@app.route("/ingredients/add", methods=["POST"])
def add_ingredient():
    if request.method == "POST":
        data = request.form.to_dict()
        
        requests.post("http://localhost:5000/ingredients/add", data=data)
        
    return redirect(url_for("admin"))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)