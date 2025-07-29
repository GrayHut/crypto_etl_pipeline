#function to get realtime crypto prices
#identify top 10 crypto and send mails and save data as csv

import requests
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

import smtplib #standard library for sending emails using the SMTP protocol
from email.mime.text import MIMEText    #module from email package to create a MIME(Multipurpose Internet Mail Extensions) object for text in an email
from email.mime.multipart import MIMEMultipart  #creates a MIME container to hold multiple components of an email ie text, attachments, images
from email.mime.base import MIMEBase    #a base class for creating MIME objects for non-text content such as files - csv, pdf
import email.encoders   #provides functions to encode MIME objects particularly for non-text attachments

#-------------------------------------------------------------------------------------------------------------------------
load_dotenv()

def email_send(subject, body, file_name, recepient):


    smtp_server='smtp.gmail.com'
    smtp_port=os.getenv('SMTP_PORT')
    sender=os.getenv('SENDER_EMAIL')
    google_app_pass=os.getenv("GOOGLE_PASS")
    #recepient='ondiekiowen@gmail.com'


    message=MIMEMultipart()
    message['From']=sender
    message['To']=', '.join(recepient)  #for multiple recepients
    message['Subject']=subject

    message.attach(MIMEText(body,'html'))

    with open(file_name, 'rb') as file:
        part=MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; file_name="{file_name}"')
        message.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, google_app_pass)
            server.sendmail(sender, recepient, message.as_string())
            print("Email sent successfully")

    except Exception as e:
        print(f"Email unable to send {e}")

#-------------------------------------------------------------------------------------------------------------------------

def crypto_data_access():

    url='https://api.coingecko.com/api/v3/coins/markets'

    parameters={
        'vs_currency':'usd',
        'order':'market_cap_desc',
        'per_page':250,
        'page':1
    }
    response=requests.get(url, params=parameters)

    if response.status_code==200:
        print("SUCCESSFULL CONNECTION!!!.... Fetching data....")

        data=response.json()
        df=pd.DataFrame(data)
        
        #selecting specific columns - data cleaning
        df=df[[
            'id','symbol','name','current_price','market_cap','high_24h','low_24h'
        ]]

        
        date_today=datetime.now().strftime('%d-%m-%Y')
        
        #adding columns
        #df['time_stamp']=date_today

        #filtering/sorting out top 10 largest coins based on current price...
        top_10_coins=df.nlargest(10, 'current_price')

        
        #saving the data as .csv
        abs_file_path=os.getenv('250_COINS_CSV_PATH')
        file_name=f'{abs_file_path}/crypto-data-for-{date_today}.csv'
        df.to_csv(file_name, index=False)
        
        print('Crypto CSV saved successfully')

        subject=f"Top crypto coins for {date_today}"
        body=f"""
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
                <style>
                    table{{
                        width:100%;
                        border-collapse:collapse;
                    }}
                    th, td{{
                        border:0.5px, solid #ddd;
                        padding:8px;
                        text-align:left;
                    }}
                    th{{
                        background-color:#F6CFFF;
                        color:white;
                    }}
                </style>
            </head>
            <body>
                <h2>Top 10 coins {date_today}</h2>
                <p>Good day!!\n</p>
                <p>These are today's top crypto coins;</p>
                
                {top_10_coins.to_html(index=False, classes='data', header=True, border=1)}

                <p>Have a nice day</p>
                <p>Regards,</p>
                <p>Grayhut Automations</p>

                <h4>@gray-hut Official</h4>
    
                
            </body>
            </html>

        """

        print("Sending email.....")

        recepient=['ondiekiowen@gmail.com', 'blackmedussa256@gmail.com']

        email_send(subject, body, file_name, recepient)



    else:
        print("ERROR ENCOUNTERED DURING CONNECTION")

#-------------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    crypto_data_access()