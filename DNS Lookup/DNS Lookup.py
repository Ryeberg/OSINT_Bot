from bs4 import BeautifulSoup
import requests
import re

#--GLOBAL VARIABLES--
    #checks domain name for common url extensions
def urlExtension(domainName):
    pattern = r'\.(com|org|net|edu|gov|mil|int)$'
    match   = re.search(pattern, domainName, re.IGNORECASE)
    
    return match is not None


    #the link: had to put this here, not a fan
def domainNameLink():
    domainName = ''
    
    while not urlExtension(domainName):
        domainName = input('Enter Domain Name: ')
        
        if not urlExtension(domainName):
            print('\nNo infomation found.\nPlease use url extensions (.com, .org, etc).\n')
        
    siteName   = 'https://check-host.net/ip-info?host='                 #dont touch
    siteToken  = '&csrf_token=4d2ba08a6cadb5a4bcc845de3d4b9a4ddbeba508' #dont touch
    
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


    #converts tag elements into strings for each table
def setTableText():
    contentToText(dbIP_tableContents,dbIP_tableContents_text)
    contentToText(ipgeolocation_tableContents,ipgeolocation_tableContents_text)
    contentToText(ip2location_tableContents,ip2location_tableContents_text)
    contentToText(geolite2_tableContents,geolite2_tableContents_text)
    contentToText(ipinfoio_tableContents,ipinfoio_tableContents_text)


    #print list with table info and none values *flag image*
def checkNoneType(table):
    tableLength = len(table)    
    for i in range(tableLength):
        if not(table[i] == None):
            print(table[i].text.strip())
        else:
            print('FORMATTING ERROR -> ',table[i])
    print('\n')


#gets the element name only from table
def getElementName(elementName):
    element = int(elementName)
        
    match element:
        case 0:
            elementName = dbIP_tableContents[element].text.strip()[:10]     #IP
        case 1:
            elementName = dbIP_tableContents[element].text.strip()[:9]      #Host Name
        case 2:
            elementName = dbIP_tableContents[element].text.strip()[:8]      #IP Range
        case 3:
            elementName = dbIP_tableContents[element].text.strip()[:3]      #ISP
        case 4:
            elementName = dbIP_tableContents[element].text.strip()[:12]     #Organization
        case 5:
            elementName = dbIP_tableContents[element].text.strip()[:7]      #Country
        case 6:
            elementName = dbIP_tableContents[element].text.strip()[:6]      #Region
        case 7:
            elementName = dbIP_tableContents[element].text.strip()[:4]      #City
        case 8:
            elementName = dbIP_tableContents[element].text.strip()[:9]      #Time Zone
        case 9:
            elementName = dbIP_tableContents[element].text.strip()[:10]     #Local Time
        case 10:
            elementName = dbIP_tableContents[element].text.strip()[:11]     #Postal Code
        
    return elementName
    
    #print the format for printElements()
def printFormat(elementName,tableName,tableContent):
    #centering the format
    longestTableName = 29
    dashes           = ( longestTableName - len(tableName) ) + 10
    
    print(f'%s\n%s{" %s" :->{dashes}}\n' %(elementName,tableName,tableContent))


    #format the content for printElements()
def contentFormat(table,element,elementLength):
    updatedContent = ''
    contentLength  = len(table[element].text.strip())

    if (contentLength + 1 == elementLength):
        return updatedContent
    else:
        match element:
            case 2:     #"3" IP Range
                updatedContent = table[element].text.strip()[elementLength + 1:-6] + ' ' + table[element].text.strip()[contentLength - 4:]
            case 5:     #"6" Country
                updatedContent = table[element].text.strip()[elementLength + 2:-5] + ' ' + table[element].text.strip()[contentLength - 4:]
            case 8:     #"9" Time Zone
                updatedContent = table[element].text.strip()[elementLength + 1:]
            case default:
                updatedContent = table[element].text.strip()[elementLength:]
    
    return updatedContent


    #num arg, prints specific element from each table
def printElements(element):
    #organize the table's name *readable*
    dbIP          = dbIP_table.a.text.strip()[:5] + ' ' + dbIP_table.a.text.strip()[6:]
    ipgeolocation = ipgeolocation_table.a.text.strip()[:16] + ' ' + ipgeolocation_table.a.text.strip()[17:]
    ip2location   = ip2location_table.a.text.strip()[:11] + ' ' + ip2location_table.a.text.strip()[12:]
    geolite2      = geolite2_table.a.text.strip()[:13] + ' ' + geolite2_table.a.text.strip()[14:]
    ipinfoio      = ipinfoio_table.a.text.strip()[:9] + ' ' + ipinfoio_table.a.text.strip()[10:]
    
    #elementName's length for getting the content
    elementLength = len( getElementName(element) ) + 1
    
    #element content
    dbIP_Content          = contentFormat(dbIP_tableContents,element,elementLength)
    ipgeolocation_Content = contentFormat(ipgeolocation_tableContents,element,elementLength)
    ip2location_Content   = contentFormat(ip2location_tableContents,element,elementLength)
    geolite2_Content      = contentFormat(geolite2_tableContents,element,elementLength)
    ipinfoio_Content      = contentFormat(ipinfoio_tableContents,element,elementLength)
    
    #print table name and elements related
    printFormat(getElementName(element),dbIP,dbIP_Content)
    printFormat(getElementName(element),ipgeolocation,ipgeolocation_Content)
    printFormat(getElementName(element),ip2location,ip2location_Content)
    printFormat(getElementName(element),geolite2,geolite2_Content)
    printFormat(getElementName(element),ipinfoio,ipinfoio_Content)


    #cleaner this way for downstairs
def strToInt(num):
    num = int(num)
    return num-1

    #print the elements header ie IP, Host Name, etc
def listHeaders():
    headerTags = []
    for i in range(len(dbIP_tableContents)):
        headerTags.insert(i, dbIP_tableContents[i].td)
        print(f'%2d. {headerTags[i].text}' %(i+1))


    #cases to select specific elements
def selectElement():
    choice = ''
    
    while not choice == 'q':
        listHeaders()
        choice = input('Select a table element, 1-11 ("q" to exit)\n')
        print()
        
        match choice:
            case '1':
                choice = strToInt(choice)   #IP
                printElements(choice)
            case '2': 
                choice = strToInt(choice)   #Host Name
                printElements(choice)
            case '3': 
                choice = strToInt(choice)   #IP Range
                printElements(choice)
            case '4': 
                choice = strToInt(choice)   #ISP
                printElements(choice)
            case '5': 
                choice = strToInt(choice)   #Organization
                printElements(choice)
            case '6':
                choice = strToInt(choice)   #Country
                printElements(choice)
            case '7': 
                choice = strToInt(choice)   #Region
                printElements(choice)
            case '8': 
                choice = strToInt(choice)   #City
                printElements(choice)
            case '9': 
                choice = strToInt(choice)   #Time Zone
                printElements(choice)
            case '10': 
                choice = strToInt(choice)   #Local Time
                printElements(choice)
            case '11': 
                choice = strToInt(choice)   #Postal Code
                printElements(choice)
            case 'q':
                print()                     #Quit
            case default:
                print('\nEnter a number from 1-11\nEnter again\n\n')   #default


    #print list with table info
def printTable(table):
    tableLength = len(table)    
    for i in range(tableLength):
        print(getElementName(i),table[i][len(getElementName(i))+2:])
    print('\n')


    #print all tables, its in the name
def printAllTables():
    print(dbIP_table.div.text.strip())
    printTable(dbIP_tableContents_text)
    
    print(ipgeolocation_table.div.text.strip())
    printTable(ipgeolocation_tableContents_text)
    
    print(ip2location_table.div.text.strip())
    printTable(ip2location_tableContents_text)
    
    print(geolite2_table.div.text.strip())
    printTable(geolite2_tableContents_text)
    
    print(ipinfoio_table.div.text.strip())
    printTable(ipinfoio_tableContents_text)


    #loop through table list, return string
def listToString(table):
    stringTable = ''
    tableLength = len(table)
    
    for i in range(tableLength):
        elementName    = getElementName(i)
        elementContent = table[i][len(getElementName(i)) + 2:]
        
        longestElementName = 12
        dashes             = ( longestElementName - len(elementName) ) + 10
        
        stringTable += f'  %s {" %s":->{dashes}}' %(elementName,elementContent) + '\n'
    
    stringTable += '\n\n'
    
    return stringTable


    #pass the text list to a single String
def passList():
    fullTable = ''
    
    fullTable += dbIP_table.div.text.strip() + '\n'
    fullTable += listToString(dbIP_tableContents_text)
    
    fullTable += ipgeolocation_table.div.text.strip() + '\n'
    fullTable += listToString(ipgeolocation_tableContents_text)
    
    fullTable += ip2location_table.div.text.strip() + '\n'
    fullTable += listToString(ip2location_tableContents_text)
    
    fullTable += geolite2_table.div.text.strip() + '\n'
    fullTable += listToString(geolite2_tableContents_text)
    
    fullTable += ipinfoio_table.div.text.strip() + '\n'
    fullTable += listToString(ipinfoio_tableContents_text)
    
    return fullTable


    #create text file and pass table info 
def writeFile():
    tables = open("newFile.txt",'w')
    tables.write(passList())
    tables.close()



#--MAIN METHOD--
def main():
    setTableText()    #pass the content to the text list
    writeFile()       #write the tables to a .txt file
    selectElement()   #menu for user to look through table elements of each table
    

#call main method
main()
