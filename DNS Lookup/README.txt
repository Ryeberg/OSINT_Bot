README

    The DNS Lookup tool is a webscraper designed to gather information about a domain name through the site www.check-host.net.
    It can only function with an internet connection and when the site is operational. If by the off-chance the website is down
    the problem should solve itself in a day or two. The tool is designed to provide supplemental information of a target's
    workplace and potentially validate their location.

NOTICE

    Participants involved in any project are fully informed about the nature, purpose, and methodologies involved, and their  
    onsent is obtained prior to participation.  This project provides an aggregate analysis derived from publicly 
    available data sources. It is crucial to acknowledge that the information presented here is intended exclusively for 
    academic and informational purposes. We firmly oppose and abstain from personally employing facial recognition technologies 
    or web scraping methods that compromise individual privacy.

INSTALLATION & IMPORT REQUIREMENTS:

    - Python 3.11 or greater
    - IDE or Python Interpreter
    - tkinter
    - beautifulSoup
    - Customtkinter
    - requests
    - re

GITHUB LINK AND FILES:

    https://github.com/Ryeberg/OSINT_Bot


CONTACT ME

    If you have any problems running the application you can email me at acald051@fiu.edu to answer all your concerning questions.
    You can also reach our github page for updates and announcements to address bugs and issues.

----------------------------------------------------------------------------------------------------------------------------------

INSTALLATION PROCEDURES BEFORE RUNNING:

    To install Python visit https://www.python.org/downloads/windows/ and select "Lastest Python 3 Release -Python #.##.#". 
    Once there scroll to the bottom until you see "Files" and select "Windows installer (64-bit)"
       
    tkinter is library that comes "pre-installed" with python standard library distributions. 
    But if not found use: pip install tk

    re or RegEx is a library pre-installed with python standard library distributions.

    To install beautifulsoup type in command prompt: pip install beaufitulsoup4 or py -m pip install beaufitulsoup4

    To install customtkinter type in command prompt: pip install customtkinter or py -m pip install customtkinter

    To install beautifulsoup type in command prompt: pip install requests or py -m pip install requests 

METHODS AND DESCRIPTIONS OF USE:

    urlExtension(domainName):                        Checks domain name for common url extensions.

    domainNameLink():                                Creates the link for the domain name.

    contentToText(tableContent,tableText):           Convert the tag elements into strings

    setTableText():                                  Converts tag elements into strings for each table.

    checkNoneType(table):                            Print list with table info and none values *flag image*.

    getElementName(elementName):                     Gets the element name only from table.

    printFormat(elementName,tableName,tableContent): Print the format for printElements().

    contentFormat(table,element,elementLength):      Format the content for printElements().

    printElements(element):                          Accepts a num argument and prints a specific element from each table.

    strToInt(num):                                   Converts a String into an int subtracted by one.

    listHeaders():                                   Print the elements header ie. IP, Host Name, etc.

    selectElement():                                 Cases to select specific elements.

    printTable(table):                               Print list with a single table info, not formatted.

    printAllTables():                                Print all tables, formatted.

    listToString(table):                             Loop through the table list, returning a string.

    passList():                                      Pass the text list to a single String.

    writeFile():                                     Create a text file and append table info.
