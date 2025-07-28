#this program aims to send the extacted crypto data via email

import smtplib #standard library for sending emails using the SMTP protocol
from email.mime.text import MIMEText    #module from email package to create a MIME(Multipurpose Internet Mail Extensions) object for text in an email
from email.mime.multipart import MIMEMultipart  #creates a MIME container to hold multiple components of an email ie text, attachments, images
from email.mime.base import MIMEBase    #a base class for creating MIME objects for non-text content such as files - csv, pdf
import email.encoders   #provides functions to encode MIME objects particularly for non-text attachments


import pandas as pd
import schedule
from datetime import datetime
import requests

def email_send(subject, body, file_name):
    smtp_server='smtp.google.com'
    smtp_port=587
    sender='ondiekiowen99@gmail.com'
    sender_pass='rexowen99@gmail.com'
    recepient='ondiekiowen@gmail.com'


    message=MIMEMultipart()
    message['From']=sender
    message['To']=recepient
    message['Subject']=subject

    message.attach(MIMEText(body,'plain'))

    with open(file_name, 'rb') as file:
        part=MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; file_name="{file_name}"')
        message.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, sender_pass)
            server.sendmail(sender, recepient, message.as_string())
            print("Email sent successfully")


    except Except as e:
        print(f"Email unable to send {e}")

