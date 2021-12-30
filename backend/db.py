import mysql.connector
from os import environ as env


mydb = mysql.connector.connect(
  host=env.get("mealsSecretHost"),
  user=env.get("mealsSecretUser"),
  password=env.get("mealsSecretKey"),
  database="meals"
)

mycursor = mydb.cursor()

if __name__ == "__main__":
    print(mydb)
    print(mycursor)