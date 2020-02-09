# Import Libraries for Accessing Ladder Capital Website
from requests_html import HTML, HTMLSession
import pandas as pd

# Import Libraries for Emailing from GMAIL
import os
import smtplib

# -------------------------------------------
# Access Ladder Capital's Front Page Website
session = HTMLSession()
r = session.get('https://laddercapital.com')

# Find and Save the Table Section Using Chrome Developer Tools
table_div = r.html.find('#top > main > div.section > div > div > div:nth-child(3)', first=True)
table = table_div.find('.table', first=True)
table_html = table.html

# Use Pandas to Convert the HTML Table into a Panda DataFrame
a = pd.read_html(table_html,index_col=0)
table_pd = a[0]

# Store the 5 Year Swap (Only First 6 Characters to Avoid the Arrow Symbol)
five = table_pd.iat[0,2][:6]

# Print the Rate Table and 5 Year Swap
print(table_pd)
print(five)

# ---------------------------------------------------------------
# Pull Gmail Login Credentials from Local Environment Variables
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# Send Email Using Gmail
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Set Email Subject and Body Content and Save it in a Message Variable
    subject = 'US Rates'
    body = f'The 5 Year Swap is {five}.'
    msg = f'Subject: {subject}\n\n{body}'

    # Send Email Message
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.encode('utf8'))