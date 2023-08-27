"""
This server side script will intercept all the requests, check them 
against a dictionary of emails and indentifying URLs, and help send
me an Email with Amazon SES alerting me that the email I sent has been opened. 
"""
import boto3
from botocore.exceptions import NoCredentialsError
import keys
from collections import defaultdict
import time
import re

#Reading from the logfile

#Dictionary ith each receiver ID, their email address, and the subject of the email sent to them
email_database = defaultdict(list)
#The receiver ID's of all the receivers who opened their emails
opened = []
#The lines that have already been read in the GET log file so that the script can tell if a new line is added
lines_seen = set()

#Refreshed the GET log file so that we start each run with a blank slate
with open("alog.txt", "w") as file:
    file.write("")

def sendEMAIL(message):
    # Set up SES client
    ses_client = boto3.client('ses', region_name='us-west-1', aws_access_key_id=keys.access_key_id, aws_secret_access_key=keys.secred_access)

    # Email details
    sender_email = keys.sender_mail
    recipient_email = keys.receiver_email
    subject = 'Someone Opened Your EMAIL'
    body = message

    # Send email
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}},
            }
        )
        print("Email sent! Message ID:", response['MessageId'])
    except NoCredentialsError:
        print("Credentials not available. Make sure you've set up AWS credentials.")

def dictionary_create():
    with open("prelog.txt", "r") as file:
        for line in file:
            key, value = line.strip().split(": ")
            address = value.split(',')[0].strip().strip("'[] ")
            sub = value.split(',')[1].strip().strip("'[] ")
            email_database[key].append(address)
            email_database[key].append(sub)



def extract_receiver_id(line):
    pattern = r'reciever_id=([a-f0-9-]+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None

def monitor_text_file(filename):

    with open(filename, 'r') as file:
        new_lines = set(file.readlines()) - lines_seen

        if new_lines:
            for line in new_lines:
                stripped_line = line.strip()
                receiver_id = extract_receiver_id(stripped_line)
                if receiver_id in email_database:
                    opened.append(receiver_id)
            lines_seen.update(new_lines)
    


def tracking():
    print("GO")
    dictionary_create()
    monitor_text_file("alog.txt")


    for r_id in opened:
        if r_id in email_database:
            #Getting the data for the SMS message based on the email_database
            email = email_database[r_id][0]
            subject = email_database[r_id][1]

            #Message to be sent via SMS
            log_text = f'Reciever "{email}" opened the email with subject "{subject}"'

            #Sends EMAIL
            sendEMAIL(log_text)
            
            #Removes the email from the data base
            del email_database[r_id]
            
            return "", 200
        else:
            return "Recipient not found", 404

if __name__ == '__main__':
    while True:
        tracking()
        time.sleep(5)
    
