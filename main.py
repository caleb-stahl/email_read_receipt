import smtplib, ssl, getpass

port = 465  # For SSL
password = input("Type your password and press enter: ")
sender_address = "youremail"
recipient_address = "youremail"
mail_text = """\
    Subject: This is a test

    If you are reading this...success!!
    
    """
# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("youremail", password)
    server.sendmail(sender_address, recipient_address, mail_text)

