"""
This server side script will intercept all the requests, check them 
against a dictionary of emails and indentifying URLs, and help send
me an SMS alerting me that the email has been opened. 
"""

from flask import Flask, request
from mail import email_database, send_mail


app = Flask(__name__)

#When a GET request involving the tracking pixel is received
#tracking() is run
@app.route("/pixel.png", methods = ["GET"])
def tracking():
    r_id = request.args.get("reciever_id")

    if r_id in email_database:
        #Getting the data for the SMS message based on the email_database
        email = email_database[r_id][0]
        subject = email_database[r_id][1]

        #Message to be sent via SMS
        log_text = f'Reciever {email} opened the email with subject {subject}'

        #Writes the message that will be sent via SMS to a log file
        with open('/path/to/email_open_log.txt', 'a') as log_file:
            log_file.write(log_text + '\n')
        
        #Removes the email from the data base
        del email_database[r_id]
        
        return "", 200
    else:
        return "Recipient not found", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    send_mail()
    
