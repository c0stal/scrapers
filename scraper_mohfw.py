import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from twilio.rest import Client


url = 'https://www.mohfw.gov.in/'

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
stats_box = soup.find('div', attrs={'class': 'site-stats-count'})
data="Total Number of Cases in India:"
for li in stats_box.findAll('li'):
    if li.text.strip() != "":
        # print(li.strong.text)
        # print(li.span.text)
        # print("==============")
        data = data+li.strong.text+'\n'
        data = data+li.span.text+'\n'
        data = data+'=============='+'\n'
        

stateData="State-wise split of Number of Cases:"
table = soup.find('table', attrs={'class':'table table-striped'})
table_header = table.find('thead')
headers = table_header.find_all('th')
cols = [ele.text.strip() for ele in headers] 
# print(cols)
stateData=stateData+','.join(cols)

table_body = table.find('tbody')
rows = table_body.find_all('tr')
stateCols=[]
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols] 
    stateData=stateData+','.join(cols)+'\n'
finalData = data+stateData

# Send message
account_sid = "account_sid"
auth_token  = "auth_token"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="<>", 
    from_="<>",
    body=finalData)