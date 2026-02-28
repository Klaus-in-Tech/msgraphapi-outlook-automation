import csv
import requests
from email_sender.ms_graph_api import get_access_token
import os
from email_sender.templates import render_template
from dotenv import load_dotenv
import time

def send_mail(subject, email_body, recipients, application_id, client_secret):
    scopes = ["https://graph.microsoft.com/Mail.Send", "https://graph.microsoft.com/Mail.ReadWrite"]
    headers = get_access_token(application_id, client_secret, scopes)
    url = "https://graph.microsoft.com/v1.0/me/sendMail"

    for addr in recipients:
        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "TEXT",
                    "content": email_body,
                },
                "toRecipients": [
                    {"emailAddress": {"address": addr}}
                ],
            },
            "saveToSentItems": "true"
        }

        try:
            response = requests.post(url, headers=headers, json=message)
            if response.status_code == 202:
                print(f"Email sent to {addr} successfully.")
            else:
                print(f"Failed to send email to {addr}: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Exception occurred while sending to {addr}: {e}")
# Example usage
if __name__ == "__main__":
 
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    subject = "OFFSHORE PROCESS AUTOMATION SERVICES - FREE PROOF OF CONCEPT"
    email_body = render_template("email.txt")

    # CSV recipients settings
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_recipients = os.path.join(project_root, "templates", "recipients.csv")
    recipients_file = os.getenv("RECIPIENTS_FILE", default_recipients)
    recipients_column = os.getenv("RECIPIENTS_COLUMN", "email")

    # read recipients from CSV
    if not os.path.exists(recipients_file):
        raise RuntimeError(f"Recipients file not found: {recipients_file}")

    with open(recipients_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if recipients_column not in headers:
            candidates = [h for h in headers if "email" in h.lower() or "to" in h.lower()]
            if candidates:
                recipients_column = candidates[0]
            else:
                raise RuntimeError(f"No recipients column found in {recipients_file}. Expected '{recipients_column}' or a column containing 'email' or 'to'.")
        recipients = []
        for row in reader:
            addr = row.get(recipients_column)
            if addr:
                addr = addr.strip()
                if addr:
                    recipients.append(addr)

    send_mail(subject, email_body, recipients, application_id, client_secret)

