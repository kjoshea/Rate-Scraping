# Import Library for Accessing Ladder Capital Website
from requests_html import HTML, HTMLSession

# Import Library for Saving Each Day's Rate
import _sqlite3

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

# Save the Rate and the Date in Proper Formats
five_year_swap = five_year_swap_element.text
date = datetime.date.today().strftime("%B %d, %Y")

# ---------------------------------------------------------------
# Save Rates into Database and Pull Saved Rates from Database
conn = _sqlite3.connect('rates.db')

c = conn.cursor()


def insert_rate():
    with conn:
        c.execute("INSERT INTO rates VALUES (:id, :rate, :date)", {'id': None,'rate': five_year_swap, 'date': date})


def get_rates():
    c.execute("SELECT * FROM rates")
    return c.fetchall()


def get_today_rate():
    c.execute("SELECT * FROM rates ORDER BY id DESC LIMIT 1")
    return c.fetchall()


def get_yesterday_rate():
    c.execute("SELECT * FROM rates ORDER BY id DESC LIMIT 1,1")
    return c.fetchall()


insert_rate()


today_rate = get_today_rate()[0][1]
yesterday_rate = get_yesterday_rate()[0][1]
today_rate_date = get_today_rate()[0][2]
yesterday_rate_date = get_yesterday_rate()[0][2]

print(today_rate)
print(yesterday_rate)

conn.close()


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
    body = f'The 5 Year Swap is {today_rate} as of {today_rate_date}.\n\n' \
           f'The 5 Year Swap was {yesterday_rate} as of {yesterday_rate_date}.'
    msg = f'Subject: {subject}\n\n{body}'

    # Send Email Message
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.encode('utf8'))
