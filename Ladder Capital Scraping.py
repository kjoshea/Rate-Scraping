from requests_html import HTML, HTMLSession
import pandas as pd

session = HTMLSession()
r = session.get('https://laddercapital.com')

table_div = r.html.find('#top > main > div.section > div > div > div:nth-child(3)', first=True)

table = table_div.find('.table', first=True)
table_html = table.html

a = pd.read_html(table_html,index_col=0)
table_pd = a[0]
five = table_pd.iat[0,2]

print(table_pd)
print(five)