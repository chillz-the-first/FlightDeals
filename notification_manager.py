import os
from twilio.rest import Client
import smtplib
from email.message import EmailMessage

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ['TWILIO_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self.sender_number = os.environ['TWILIO_VIRTUAL_NUMBER']
        self.receiver_number = os.environ['TWILIO_WHATSAPP_NUMBER']
        self.sender_email = os.environ['SENDER_EMAIL']
        self.app_password = os.environ['GMAIL_APP_PASSWORD']
        self.server = os.environ['SMTP_SERVER']

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

    def send_email(self, flight, users):
        print("Sending email.")
        if not self.sender_email or not self.app_password:
            print("CRITICAL: Email credentials are missing in .env")
            return

        text = (f"Only R{flight.price} to fly from {flight.origin_airport} to {flight.destination_airport}"
                f", with {flight.stops} stop(s) departing {flight.out_date} and returning on {flight.return_date}")

        msg = EmailMessage()
        msg['Subject'] = '✈️ Cheap Flight Alert!'
        msg['From'] = self.sender_email
        # msg['To'] = recipient_email

        msg.set_content(text)

        for user in users:
            if "emailAddress" not in user:
                print("Row is empty in google sheet, so no user email address found")
                continue

            recipient = user["emailAddress"]
            msg['To'] = recipient
            try:
                with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                    connection.starttls()

                    connection.login(user=self.sender_email, password=self.app_password)

                    connection.send_message(msg)

                    print("Email sent successfully!")

            except smtplib.SMTPAuthenticationError:
                print("Error: Authentication failed. Did you use your normal password instead of an App Password?")
            except Exception as e:
                print(f"An error occurred: {e}")

    def send_emails(self, flight, users):
        print("Sending email.")
        if not self.sender_email or not self.app_password:
            print("CRITICAL: Email credentials are missing in .env")
            return

        email_body = (f"Only R{flight.price} to fly from {flight.origin_airport} to {flight.destination_airport}"
                f", with {flight.stops} stop(s) departing {flight.out_date} and returning on {flight.return_date}")

        for user in users:
            if "emailAddress" not in user:
                print("Row is empty in google sheet, so no user email address found")
                continue

            recipient = user["emailAddress"]

            with smtplib.SMTP(self.server, 587) as connection:
                connection.starttls()
                connection.login(self.sender_email, self.app_password)
                connection.sendmail(
                    from_addr=self.sender_email,
                    to_addrs=recipient,
                    msg=f"Subject:✈️ Cheap Flight Alert!!\n\n{email_body}".encode('utf-8')
                )

