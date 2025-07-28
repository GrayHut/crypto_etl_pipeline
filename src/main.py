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

def email_send(subject, body, file_name, recepient):

    load_dotenv()

    smtp_server='smtp.gmail.com'
    smtp_port=587
    sender='ondiekiowen99@gmail.com'
    google_app_pass=os.getenv("GOOGLE_PASS")
    #recepient='ondiekiowen@gmail.com'


    message=MIMEMultipart()
    message['From']=sender
    message['To']=', '.join(recepient)
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

        #selecting the top 10 most expensive coins
        # most_expensive_coins=df.sort_values(by='current_price', ascending=False)
        # top_10_coins=most_expensive_coins.head(10)
        # top_10_coins.to_csv(f'media/10_most_expensive_{date_today}.csv', index=False)

        top_10_coins=df.nlargest(10, 'current_price')

        # if top_10_coins:
        #     print('Top 10 coins exist')
        # else:
        #     print('Top10 Error')

        #saving the data as .csv
        file_name=f'/media/gray-hut/E/Edu/LuxDev/luxfiles/projects/crypto_etl_pipeline/media/crypto-data-for-{date_today}.csv'
        df.to_csv(file_name, index=False)
        # file_name_2=f'/media/gray-hut/E/Edu/LuxDev/luxfiles/projects/crypto_etl_pipeline/media/top-10-{date_today}.csv'
        # top_10_coins.to_csv(file_name_2)
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