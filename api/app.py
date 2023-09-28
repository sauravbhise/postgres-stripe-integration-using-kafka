from flask import Flask, request, jsonify
from database.app import Database
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

app = Flask(__name__)

db = Database(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    port=5432,
)

db.connect()


@app.route("/customers", methods=["GET"])
def get_customers():
    result = db.select_data("customers")
    customers = []
    for row in result:
        customers.append({"id": row[0], "name": row[1], "email": row[2]})
    return jsonify(customers)


@app.route("/customers/<id>", methods=["GET"])
def get_customer(id):
    result = db.select_data("customers", "*", f"id={id}")
    customer = result.fetchone()
    if customer:
        return jsonify({"id": customer[0], "name": customer[1], "email": customer[2]})
    else:
        return jsonify({"message": "Customer not found"}), 404


@app.route("/customers", methods=["POST"])
def create_customer():
    data = request.json
    name = data["name"]
    email = data["email"]

    db.insert_data("customers", "name, email", (name, email))
    return jsonify({"message": "Customer created successfully"}), 201


@app.route("/customers/<id>", methods=["PUT"])
def update_customer(id):
    data = request.json
    name = data["name"]
    email = data["email"]

    db.update_data("customers", f"name='{name}', email='{email}'", f"id={id}")
    return jsonify({"message": "Customer updated successfully"})


@app.route("/customers/<id>", methods=["DELETE"])
def delete_customer(id):
    db.delete_data("customers", f"id={id}")
    return jsonify({"message": "Customer deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
