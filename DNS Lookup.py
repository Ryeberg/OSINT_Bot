from bs4 import BeautifulSoup
import requests

#--GLOBAL VARIABLES--
    #the link: had to put this here, not a fan
def domainNameLink():
domainName = input('Enter Domain Name: ')

siteName   = 'https://check-host.net/ip-info?host='
siteToken  = '&csrf_token=4d2ba08a6cadb5a4bcc845de3d4b9a4ddbeba508'

return siteName+domainName+siteToken


    #get html
siteHtml = requests.get(domainNameLink()).text
soup     = BeautifulSoup(siteHtml,'lxml')

    #filter info for tables
tables = soup.find('div',id='content2')

dbIP_table          = tables.find('div',id='ip_info-dbip')    
ipgeolocation_table = tables.find('div',id='ip_info-ipgeolocation')
ip2location_table   = tables.find('div',id='ip_info-ip2location')
geolite2_table      = tables.find('div',id='ip_info-geolite2')
ipinfoio_table      = tables.find('div',id='ip_info-ipinfoio')

    #tables info only *no map data*
dbIP_tableContents          = dbIP_table.find_all('tr')
ipgeolocation_tableContents = ipgeolocation_table.find_all('tr')
ip2location_tableContents   = ip2location_table.find_all('tr')
geolite2_tableContents      = geolite2_table.find_all('tr')
ipinfoio_tableContents      = ipinfoio_table.find_all('tr')

    #list to collect the tables data for improving readability 
dbIP_tableContents_text          = []
ipgeolocation_tableContents_text = []
ip2location_tableContents_text   = []
geolite2_tableContents_text      = []
ipinfoio_tableContents_text      = []


#--METHODS--
    #convert the tag elements into strings
def contentToText(tableContent,tableText):
    tableLength =len(tableContent)
    for i in range(tableLength):
        tableText.insert( i,tableContent[i].text.replace('\n',' ') )


    #print list with specific table info
def printTableElement(table):
    tableLength = len(table)    
    for i in range(tableLength):
        if not(table[i] == None):
            print(table[i].text.strip())
        else:
            print('FORMATTING ERROR -> ',table[i])
    print('\n')


    #print list with table info
def printTable(table):
    tableLength = len(table)    
    for i in range(tableLength):
        print(table[i])
    print('\n')


    #print all tables, its in the name
def printAllTables():
    printTable(dbIP_tableContents_text)
    printTable(ipgeolocation_tableContents_text)
    printTable(ip2location_tableContents_text)
    printTable(geolite2_tableContents_text)
    printTable(ipinfoio_tableContents_text)


#--MAIN METHOD--
def main():
    #pass the content to the list
    contentToText(dbIP_tableContents,dbIP_tableContents_text)
    contentToText(ipgeolocation_tableContents,ipgeolocation_tableContents_text)
    contentToText(ip2location_tableContents,ip2location_tableContents_text)
    contentToText(geolite2_tableContents,geolite2_tableContents_text)
    contentToText(ipinfoio_tableContents,ipinfoio_tableContents_text)
    
    #print database name and table
    print(dbIP_table.div.text.strip())
    printTable(dbIP_tableContents_text)


#call main method
main()
