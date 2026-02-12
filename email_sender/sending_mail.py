import requests
from email_sender.ms_graph_api import get_access_token
import os
from email_sender.templates import render_template
from dotenv import load_dotenv

def send_mail(subject, body_html, to_emails, application_id, client_secret):
    scopes = ["https://graph.microsoft.com/Mail.Send"]
    headers = get_access_token(application_id, client_secret, scopes)
    url = "https://graph.microsoft.com/v1.0/me/sendMail"

    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body_html,
            },
            "toRecipients": [
                {"emailAddress": {"address": addr}} for addr in to_emails
            ],
        },
        "saveToSentItems": "true"
    }

    response = requests.post(url, headers=headers, json=message)
    if response.status_code == 202:
        print("Email sent successfully.")
    else:
        print(f"Failed to send email: {response.status_code} {response.text}")

# Example usage
if __name__ == "__main__":
 
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    subject = "Test Email"
    body_html = render_template("email.txt", {"recipient_name": "Klaus"})
    to_emails = ["kkallan07@gmail.com"]

    send_mail(subject, body_html, to_emails, application_id, client_secret)