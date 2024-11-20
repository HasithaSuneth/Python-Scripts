import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP configuration
SMTP_SERVER = "smtp.example.com"  # Replace with your SMTP server
SMTP_PORT = 587  # Typically 587 for TLS, 465 for SSL
EMAIL_ADDRESS = "your_email@example.com"  # Your email address
EMAIL_PASSWORD = "your_password"  # Your email password

# Recipient configuration
RECIPIENT_EMAIL = "recipient_email@example.com"  # Test recipient email

# Email content
SUBJECT = "SMTP Test Email"
BODY = """\
Hi,

This is a test email sent from the SMTP Email Tester script.

Best regards,
Your SMTP Tester
"""

def send_email():
    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = SUBJECT
        msg.attach(MIMEText(BODY, "plain"))
        
        # Connect to the SMTP server
        print("Connecting to SMTP server...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to secure
            print("Logging in...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("Sending email...")
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the tester
if __name__ == "__main__":
    send_email()
