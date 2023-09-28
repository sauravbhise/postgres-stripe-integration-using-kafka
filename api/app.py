from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2
from decouple import config


app = Flask(__name__)
api = Api(app)

DATABASE_NAME = config("DATABASE_NAME")
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT")

conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
)


class CustomerResource(Resource):
    def get(self, customer_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        if customer:
            return {"id": customer[0], "name": customer[1], "email": customer[2]}, 200
        else:
            return {"message": "Customer not found"}, 404

    def put(self, customer_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("email")
        args = parser.parse_args()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE customers SET name = %s, email = %s WHERE id = %s",
            (args["name"], args["email"], customer_id),
        )
        conn.commit()
        cursor.close()
        return {"message": "Customer updated successfully"}, 200

    def delete(self, customer_id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()
        cursor.close()
        return {"message": "Customer deleted successfully"}, 200


class CustomerListResource(Resource):
    def get(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        cursor.close()
        customer_list = [{"id": c[0], "name": c[1], "email": c[2]} for c in customers]
        return customer_list, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("email", required=True)
        args = parser.parse_args()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email) VALUES (%s, %s)",
            (args["name"], args["email"]),
        )
        conn.commit()
        cursor.close()
        return {"message": "Customer created successfully"}, 201


api.add_resource(CustomerListResource, "/customers")
api.add_resource(CustomerResource, "/customers/<int:customer_id>")

if __name__ == "__main__":
    app.run(debug=True)
