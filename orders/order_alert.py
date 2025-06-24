import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from .models import Order
from .models import PhoneAlert

def get_message(order):
    message = []
    address = order.shipping_address

    message.append(f"An order totalling ${order.total_amount} has been placed")
    message.append("Shipping adress:")
    message.append(f"{address.street_address}")
    message.append(f"{address.city}, {address.state} {address.postal_code}")
    message.append(f"{address.country}")

    return "\n".join(message)

def notify_order(order):
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    # Carrier domain lookup table
    CARRIER_GATEWAYS = {
        "att": "@txt.att.net",
        "verizon": "@vtext.com",
        "tmobile": "@tmomail.net",
        "sprint": "@messaging.sprintpcs.com",
        "boost": "@myboostmobile.com"
    }

    for phone in PhoneAlert.objects.iterator():
        to_email = f"{phone.number}{CARRIER_GATEWAYS[phone.carrier]}"
        msg = EmailMessage()
        msg.set_content(get_message(order))
        msg['Subject'] = "Order Notification"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
        except Exception as e:
            pass