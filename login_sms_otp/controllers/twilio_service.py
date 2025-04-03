from odoo import http
from odoo.http import request
from twilio.rest import Client


class TwilioSMSService:
    @staticmethod
    def send_sms(phone_number, message):
        # Your Twilio credentials (make sure to keep them secure)
        twilio_sid = ""  # Replace with your Twilio Account SID
        twilio_auth_token = ""  # Replace with your Twilio Auth Token
        twilio_phone_number = ''  # Replace with your Twilio phone number

        # Initialize the Twilio client
        client = Client(twilio_sid, twilio_auth_token)

        try:
            # Send the SMS
            message_sent = client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=phone_number  # The recipient's phone number
            )

            return {'status': 'success', 'sid': message_sent.sid}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}