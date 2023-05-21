import smtplib, ssl, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL
password = getpass.getpass("Type your password and press enter: ")
sender_address = "youremail"
recipient_address = "youremail"

message = MIMEMultipart()
message["Subject"] = "First Test"
message["From"] = sender_address
message["To"] = recipient_address

image_link = "image_link"
mail_text = """\

    If you are reading this...success (pt3)!!

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
    server.login("youremail", password)
    server.sendmail(sender_address, recipient_address, message.as_string())
