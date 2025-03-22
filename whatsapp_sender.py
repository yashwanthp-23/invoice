# bot/whatsapp_sender.py
from twilio.rest import Client
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = "whatsapp:+14155238886"

client = MongoClient("mongodb://localhost:27017/")
db = client["invoice_bot"]

twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

def send_whatsapp_message(customer_id, file_path):
    customer = db.customers.find_one({"customer_id": customer_id})
    to = f"whatsapp:{customer['phone']}"

    message = twilio_client.messages.create(
        from_=FROM_WHATSAPP,
        to=to,
        body="Your invoice is ready.",
        media_url=[f"https://your-public-url.com/{file_path}"]  # Upload file to S3 or use a public link
    )
    return message.sid
