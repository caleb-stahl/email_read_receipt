import smtplib, ssl, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_id import main_gen

email_database = {}

def send_mail():
    while True:
        port = 465  # For SSL
        password = getpass.getpass("Type your password and press enter: ")
        sender_address = "your_email@gmail.com"
        recipient_address = input("Type in the receivers email address: ")
        subject = input("Enter the email Subject Line: ")

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender_address
        message["To"] = recipient_address

        #Get the unique recipent identifier for the email
        image_link, dict_key = main_gen()
        #Store it in the database
        email_database[dict_key] = [recipient_address, subject]


        #Allows me to format a new email
        print("Enter the email message (press Ctrl+D on a new line to finish):")
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break

        #Makes the email that is sent the same format as I entered it in. 
        mail_message = "\n".join(lines)
        mail_message = mail_message.replace("\n", "<br>")


        #HTML code that is formatted how the email will look. 
        mail_text = """\
            <html>
                <head></head>
                <body>
                    <p>
                        {mail_message}
                    </p>
                    <p>
                        <img src = "{image_link}">
                    </p>
                </body>
            </html>

            
            """
        mail_text = mail_text.format(image_link=image_link, mail_message=mail_message)
        msg_parsed = MIMEText(mail_text, "html")
        message.attach(msg_parsed)

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("your_email@gmail.com", password)
            server.sendmail(sender_address, recipient_address, message.as_string())
        
if __name__ == "__main__":
    send_mail()


