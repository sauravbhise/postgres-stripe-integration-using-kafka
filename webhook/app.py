import json
import os
import stripe
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from database.app import Database


load_dotenv()


stripe.api_key = os.getenv("STRIPE_API_KEY")
endpoint_secret = os.getenv("STRIPE_ENDPOINT_SECRET")

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")


db = Database(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    port=5432,
)

app = Flask(__name__)

db.connect()


@app.route("/webhook", methods=["POST"])
def webhook():
    event = None
    payload = request.data.decode("utf-8")
    sig_header = request.headers["STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event["type"] == "customer.created":
        customer = event["data"]["object"]
        id = customer["id"]
        name = customer["name"]
        email = customer["email"]
        db.insert_data("customers", "id, name, email", (id, name, email))
        print(customer)
    elif event["type"] == "customer.deleted":
        customer = event["data"]["object"]
        id = customer["id"]
        db.delete_data("customers", f"id='{id}'")
    elif event["type"] == "customer.updated":
        customer = event["data"]["object"]
        id = customer["id"]
        name = customer["name"]
        email = customer["email"]
        db.update_data("customers", f"name='{name}', email='{email}'", f"id='{id}'")
    else:
        print("Unhandled event type {}".format(event["type"]))

    return jsonify(success=True)
