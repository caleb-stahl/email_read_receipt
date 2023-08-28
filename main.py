"""
This server side script checks an access log file (alog) for GET requests pertaining
to the tracking pixel. Once it compiles a dictionary based off the emails we are tracking
(which is logged by mail.py), it checks to see if any of the reciever IDs that are in alog
are also in the dictionary of the email's we wanted to track, sending me an Email with 
Amazon SES alerting of the recipients email address as well as the subject line of the email
that I was tracking. 
"""
import boto3
from botocore.exceptions import NoCredentialsError
import keys
from collections import defaultdict
import time
import re


#Dictionary with each receiver ID, their email address, and the subject of the email sent to them
email_database = defaultdict(list)
#The receiver IDs of all the receivers who opened their emails
opened = []
#The lines that have already been read in the GET log file so that the script can tell if a new line is added (used in monitor_text_file)
lines_seen = set()

#Refreshed the GET log file so that we start each run with a blank slate
with open("alog.txt", "w") as file:
    file.write("")

"""
This function is responsible for sending emails with Amazon SES
"""
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
    #Makes a dictionary of the recipient ID, email address, and subject line of the email that mail.py logs 
    with open("prelog.txt", "r") as file:
        for line in file:
            key, value = line.strip().split(": ")
            address = value.split(',')[0].strip().strip("'[] ")
            sub = value.split(',')[1].strip().strip("'[] ")
            email_database[key].append(address)
            email_database[key].append(sub)
    #Wipes the file after the dictionary is creates
    with open("prelog.txt", "w") as file:
        file.write("")


"""
Helper function to monitor_text_file() that pulls our generated
reciever IDs from GET requests relating to our tracking pixel
"""
def extract_receiver_id(line):
    pattern = r'reciever_id=([a-f0-9-]+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None

"""
This function monitors alog, our log file that stores GET requests relating to 
our tracking pixel. 
"""
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
    

"""
The "meat and potatoes" of main.py
Culmintates the above functions to send me an email alerting me 
that one of the emails I wanted to track has been opened. 
"""
def tracking():
    #Create dictionary from the log file made by mail.py
    dictionary_create()
    #Create a list of all the recipient IDs that have opened their email 
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
            
            return ""
        else:
            return "Recipient not found"

if __name__ == '__main__':
    while True:
        tracking()
        time.sleep(5)
    
