import os
from twilio.rest import Client

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ['TWILIO_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self.sender_number = os.environ['TWILIO_VIRTUAL_NUMBER']
        self.receiver_number = os.environ['TWILIO_WHATSAPP_NUMBER']

    def send_notification(self, flight):
        print("Sending notification.")
        text = (f"Only R{flight.price} to fly from {flight.origin_airport} to {flight.destination_airport}"
                f", on {flight.out_date} until {flight.return_date}")

        message = self.client.messages.create(
            from_=f"whatsapp:{self.sender_number}",
            to=f"whatsapp:{self.receiver_number}",
            body=text
        )

        print(f"Message sent successfully! SID: {message.sid}")