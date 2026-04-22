import os
from twilio.rest import Client
import smtplib
from email.message import EmailMessage

class NotificationManager:
    """Handles all outbound notifications: WhatsApp (Twilio) and email (Gmail SMTP).
    This class is responsible for sending notifications with the deal flight details."""
    def __init__(self):
        self.account_sid = os.environ['TWILIO_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self.sender_number = os.environ['TWILIO_VIRTUAL_NUMBER']
        self.receiver_number = os.environ['TWILIO_WHATSAPP_NUMBER']
        self.sender_email = os.environ['SENDER_EMAIL']
        self.app_password = os.environ['GMAIL_APP_PASSWORD']
        self.server = os.environ['SMTP_SERVER']
        #
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')

    def build_message(self, flight):
        """Private helper: format the deal text from a FlightData object."""
        return (
            f"Only R{flight.price} to fly from {flight.origin_airport} to {flight.destination_airport}"
            f" with {flight.stops} stop(s), departing {flight.out_date} and returning {flight.return_date}."
        )


    def send_notification(self, flight):
        """Send a WhatsApp message via Twilio."""
        print("Sending Whatsapp notification.")
        message = self.client.messages.create(
            from_=f"whatsapp:{self.sender_number}",
            to=f"whatsapp:{self.receiver_number}",
            body=self.build_message(flight),
        )

        print(f"Message sent successfully! SID: {message.sid}")

    def send_emails(self, flight, users):
        """Send a deal alert email to every user in the list.
        pens a single SMTP connection for all recipients instead of reconnecting for each user."""
        print("Sending email.")

        if not self.sender_email or not self.app_password:
            print("CRITICAL: Email credentials are missing in .env")
            return

        email_body = self.build_message(flight)

        try:
            with smtplib.SMTP(self.smtp_server, port=587) as connection:
                connection.starttls()
                connection.login(self.sender_email, self.app_password)

                for user in users:
                    recipient = user["emailAddress"]
                    if not recipient:
                        print("Skipping row with no email address.")
                        continue

                    # Build a fresh EmailMessage per recipient (avoids stale To: headers)
                    msg = EmailMessage()
                    msg['Subject'] = '✈️ Cheap Flight Alert!'
                    msg['From'] = self.sender_email
                    msg['To'] = recipient
                    msg.set_content(email_body)

                    connection.send_message(msg)
                    print(f"Email sent to: {recipient}")
        except smtplib.SMTPAuthenticationError:
            print("Auth failed — are you using a Gmail App Password, not your normal password?")
        except Exception as e:
            print(f"Email error: {e}")

