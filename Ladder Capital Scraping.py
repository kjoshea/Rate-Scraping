# Import Library for Accessing Ladder Capital Website
from requests_html import HTML, HTMLSession

# Import Libraries for Emailing from Gmail
import os
import smtplib

# Import Library for Dates and Times
import datetime

# -------------------------------------------
# Access Ladder Capital's Front Page Website
session = HTMLSession()
r = session.get('https://laddercapital.com')

# Render Ladder Capital's Website to get Updated Rate
r.html.render()

# Identify Rate Element with CSS Selector
five_year_swap_element = r.html.find('#financity-page-wrapper > div.gdlr-core-page-builder-body '
                                     '> div.gdlr-core-pbf-wrapper.home-finance-box'
                                     ' > div.gdlr-core-pbf-wrapper-content.gdlr-core-js > div > div > div > div > div'
                                     ' > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(4) > span'
                                     , first=True)

# Save the Text of the Rate Element and Print to Screen
five_year_swap = five_year_swap_element.text
print(five_year_swap)

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
    subject = '5 Year Swap'
    body = f'The 5 Year Swap is {five_year_swap}'
    date = datetime.date.today().strftime("%B %d, %Y")
    msg = f'Subject: {subject}\n\n{body}\n\nAs of {date}'

    # Send Email Message
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.encode('utf8'))
