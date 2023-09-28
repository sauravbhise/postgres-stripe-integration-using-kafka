import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")


def add_customer(id, name, email):
    try:
        customer = stripe.Customer.create(id=id, name=name, email=email)
        return customer
    except stripe.error.StripeError as e:
        print(f"Error creating customer: {e}")
        return None


def read_customer(id):
    try:
        customer = stripe.Customer.retrieve(id)
        return customer
    except stripe.error.StripeError as e:
        print(f"Error retrieving customer: {e}")
        return None


def update_customer(id, name, email):
    try:
        customer = stripe.Customer.modify(id, name=name, email=email)
        return customer
    except stripe.error.StripeError as e:
        print(f"Error updating customer: {e}")
        return None


def delete_customer(id):
    try:
        customer = stripe.Customer.retrieve(id)
        customer.delete()
        return True
    except stripe.error.StripeError as e:
        print(f"Error deleting customer: {e}")
        return False
