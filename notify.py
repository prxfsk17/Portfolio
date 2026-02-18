import os
from dotenv import load_dotenv
from datetime import datetime
import smtplib
from email.message import EmailMessage
import threading

class Notify:

    def __init__(self):
        load_dotenv()
        self.sender_email = os.getenv("SENDER_MAIL")
        self.recipient_email = os.getenv("RECIPIENT_MAIL")
        self.password = os.getenv("PASSWORD_MAIL")

    def send_async_email(self, email, subject, message):
        thread = threading.Thread(
            target=self.send_message,
            args=(email, subject, message)
        )
        thread.start()

    def send_message(self, email, subject, message):

        new_subject = f"{datetime.now().strftime('%d.%m.%Y')} - {subject}"
        email_content = f"{message}\n\nSent from: {email}"

        msg = EmailMessage()
        msg.set_content(email_content)
        msg['Subject'] = new_subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(user=self.sender_email, password=self.password)
                errors = server.send_message(msg)

                if not errors:
                    return "✅ Thank you for your message!"
                else:
                    print(f" : {errors}")
                    return "⚠️ Unfortunately, your message wasn't sent, try later."

        except Exception as e:
            print(f"❌: {e}")
            return "⚠️ Unfortunately, your message wasn't sent, try later."

