"""
This server side script will intercept all the requests, check them 
against a dictionary of emails and indentifying URLs, and help send
me an SMS alerting me that the email has been opened. 
"""

from flask import Flask, request
from email import email_database, send_mail


app = Flask(__name__)


@app.route("/pixel.png", methods = ["GET"])

def tracking():
    r_id = request.args.get("reciever_id")

    if r_id in email_database:
        email = email_database[r_id][0]
        subject = email_database[r_id][1]

        log_text = f'Reciever {email} opened the email with subject {subject}'

        with open('/path/to/email_open_log.txt', 'a') as log_file:
            log_file.write(log_text + '\n')
        
        return "", 200
    else:
        return "Recipient not found", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    send_mail()
    
