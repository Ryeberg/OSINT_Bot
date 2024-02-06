#PYAUTOGUI



#BEUTIFULSOUP
from bs4 import BeautifulSoup
import requests
import array as arr

html_text        = requests.get('https://check-host.net/ip-info?host=fiu.edu&csrf_token=0400d10481d0c9370e37d5b5af615deb27b183b0').text
html_text_backup = requests.get('https://brilliant.org/').text
soup             = BeautifulSoup(html_text, 'lxml')   

tables = soup.find('div',id='content2')

dbIP_table              = tables.find('div',id='ip_info-dbip')
dbIP_tableContents      = dbIP_table.find_all('tr')
dbIP_tableContents_text = arr.array('i')

for i in range(11):
    dbIP_tableContents_text.insert(dbIP_tableContents[i].text.replace('\n',' ').strip())

print(dbIP_tableContents_text)
