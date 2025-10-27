import os
from flask import Flask # type: ignore
from flask_mail import Mail, Message # type: ignore
from dotenv import load_dotenv #type: ignore
from datetime import datetime

LOG_FILE = "email_test_log.md"
recipient_list = ['DWatson@hcc-nd.edu','akromah@hcc-nd.edu']

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

    return app

def log_to_markdown(lines):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n## Email Test — {timestamp}\n")
        for line in lines:
            f.write(f"- {line}\n")

def run_email_test(send_email=False):
    app = create_app()
    mail = Mail(app)

    results = []
    tips = []

    with app.app_context():
        username = app.config.get("MAIL_USERNAME")
        password = app.config.get("MAIL_PASSWORD")
        default_sender = app.config.get("MAIL_DEFAULT_SENDER")

        print(" Config Check:")
        print("MAIL_USERNAME:", username)
        print("MAIL_PASSWORD:", " Loaded" if password else " Missing")
        print("MAIL_DEFAULT_SENDER:", default_sender)

        results.append(f"MAIL_USERNAME: {username or 'Missing'}")
        results.append(f"MAIL_PASSWORD: {' Loaded' if password else ' Missing'}")
        results.append(f"MAIL_DEFAULT_SENDER: {default_sender or ' Missing'}")

        if not username:
            tips.append(" MAIL_USERNAME is missing. Check your `.env` file and confirm `MAIL_USERNAME=your_gmail_address@gmail.com` is set.")
        if not password:
            tips.append(" MAIL_PASSWORD is missing. Make sure you're using a Gmail app password, not your regular password.")
        if not default_sender:
            tips.append(" MAIL_DEFAULT_SENDER is not set. You can add `MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')` to `config.py`.")

        msg = Message(
            subject="Test Email from Flask",
            recipients=recipient_list if recipient_list else [],
            body="This is a test email sent from your Flask app."
        )

        print("\n Message Object:")
        print("Subject:", msg.subject)
        print("Recipients:", msg.recipients)
        print("Sender:", msg.sender)

        results.append(f"Message Subject: {msg.subject}")
        results.append(f"Message Recipients: {msg.recipients}")
        results.append(f"Message Sender: {msg.sender}")

        if send_email:
            try:
                mail.send(msg)
                print("\n Email sent successfully!")
                results.append(" Email sent successfully.")
            except Exception as e:
                print("\n Email failed to send:")
                print(e)
                results.append(f" Email failed to send: {e}")
        else:
            print("\n Dry-run complete. No email sent.")
            results.append(" Dry-run complete. No email sent.")

        if tips:
            print("\n Recovery Tips:")
            for tip in tips:
                print(tip)
                results.append(tip)

        log_to_markdown(results)

if __name__ == "__main__":
    run_email_test(send_email=True)  # Change to True to send