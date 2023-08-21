"""
This server side script will intercept all the requests, check them 
against a dictionary of emails and indentifying URLs, and help send
me an SMS alerting me that the email has been opened. 
"""

from flask import Flask, request

app = Flask(__name__)

email_database = {}

@app.route("/pixel.png", methods = ["GET"])

def tracking():
    r_id = request.args.get("reciever_id")

    if r_id in email_database:
        email = email_database[r_id][0]
        subject = email_database[r_id][1]

        log_text = f'Reciever {email} opened the email with subject {subject}'

        with open('/path/to/email_open_log.txt', 'a') as log_file:
            log_file.write(log_text + '\n')
        
        return ""
    else:
        return "Recipient not found"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    
