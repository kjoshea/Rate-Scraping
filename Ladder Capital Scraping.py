from requests_html import HTML, HTMLSession
import pandas as pd

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

# Store the 5 Year Swap
five = table_pd.iat[0,2]

# Print the Rate Table and 5 Year Swap
print(table_pd)
print(five)



