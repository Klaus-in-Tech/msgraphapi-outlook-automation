Email Automation with Microsoft Outlook (Graph API)
===================================================

Simple Python project to send templated emails through Microsoft Outlook using the Microsoft Graph API.

Quick Start
-----------

1. **Create a virtual environment and install dependencies:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Register an application in Microsoft Azure:**

- Go to [Azure Portal](https://portal.azure.com/) and navigate to **Azure Active Directory** > **App registrations** > **New registration**.
- Set a name for your app and choose supported account types.
- After registration, note the **Application (client) ID**.
- Go to **Certificates & secrets** and create a new **Client secret**. Save the value.
- Under **API permissions**, add permissions for `Mail.Send` and `Mail.ReadWrite` under Microsoft Graph. Click **Grant admin consent** if needed.

3. **Copy and edit `.env.example` to `.env` with your Microsoft Graph credentials:**

- `APPLICATION_ID` = Application (client) ID from Azure
- `CLIENT_SECRET` = Client secret value from Azure
- Optionally, set `RECIPIENTS_FILE` and `RECIPIENTS_COLUMN` for custom CSV paths.

4. **Prepare your email template and recipients list:**

- Place your email template in `email_sender/templates/email.txt`.
- Add recipient emails in `templates/recipients.csv` (default column: `email`).

5. **Send emails:**

```bash
PYTHONPATH=. python -m email_sender.sending_mail
```

- The script reads recipients from the CSV file and sends emails individually.
- Each email is sent using Microsoft Graph API and exceptions are handled per recipient.

Notes
-----

- The project uses Microsoft Graph API for sending emails.
- Email templates are rendered using the `render_template` function.
- Recipients are loaded from a CSV file; you can customize the column name via `.env`.
- For higher-volume sending, consider adding longer delays or using a queued worker.
- Do not commit `.env` to version control. Use a secrets manager for production.

Project Structure
-----------------

- `email_sender/ms_graph_api.py`: Handles authentication with Microsoft Graph.
- `email_sender/sending_mail.py`: Main script for sending emails.
- `email_sender/templates.py`: Template rendering utilities.
- `templates/recipients.csv`: List of recipient email addresses.