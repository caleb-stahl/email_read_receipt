import smtplib, ssl, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_id import main_gen
from tracker import *

port = 465  # For SSL
password = getpass.getpass("Type your password and press enter: ")
sender_address = "sender email"
recipient_address = "reciver email"
subject = "Your email subject"

message = MIMEMultipart()
message["Subject"] = subject
message["From"] = sender_address
message["To"] = recipient_address


image_link, dict_key = main_gen()

email_database[dict_key] = [recipient_address, subject]


mail_text = """\

    If you are reading this...success!!

    <html>
        <head></head>
        <body>
            <p>
                <img src = "{0}">
            </p>
        </body>
    </html>

    
    """
mail_text = mail_text.format(image_link)
msg_parsed = MIMEText(mail_text, "html")
message.attach(msg_parsed)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("sender email", password)
    server.sendmail(sender_address, recipient_address, message.as_string())


