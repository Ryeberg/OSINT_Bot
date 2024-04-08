from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import pyautogui
import time
import pyperclip
import re
import os
import pywinstyles
import requests
import customtkinter as ctk


# Global Variables
hidden_text_id = None
default_folder = "Evidence"
default_file = "Image Forensic Report"
folder_path = None
file_path = None
domain_name = None


# Future project but for now this portion does not work and may need further testing
def toggle_hidden_text():
    global hidden_text_id

    if selected_os.get() == "":
        # Hidden text for "Please Select OS"
        hidden_text = ctk.CTkLabel(master=container2,
                                   text="Please Select OS",
                                   font=("Arial", 14, "bold"),
                                   text_color="dark red")
        hidden_text_id = hidden_text.place(x=450, y=70)
    else:
        return


# Function for browsing file path
def browse(text_field):

    selected_path = filedialog.askdirectory() if text_field == text_field1 else filedialog.askopenfilename()
    text_field.delete(0, "end")
    text_field.insert(0, selected_path)


# Used to chronologically results from image search in Tinyeye.
def extract_date(capture):
    date_str = capture.find('span', class_="crawl-date").text
    # re.search()searches for the first occurrence of a pattern within a string.
    # (\w+ \d+ \d+) is a pattern that searches a word first then two integers like a date: May, 13, 1994
    match = re.search(r'(\w+ \d+, \d+)', date_str)
    if match:
        # group(0) is referring to the entire matched substring
        date_str = match.group(0)
        # datetime.strip time converts the date string to a datetime object for sorting
        return datetime.strptime(date_str, "%b %d, %Y")
    else:
        # If no date is found, return a default string
        return datetime.min


# The second step process for the bot automation specifically used for Tinyeye
def tiny_collect():
    time.sleep(3)
    # Allows pyautogui to simulate combination keys such as holding down the ctrl button

    # This is to select the url
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'c')

    # pyperclip is a libray that allows you to copy to a clipboard through python
    url_copy = pyperclip.paste()

    # Future code will involve multiple browsers
    driver = webdriver.Firefox()
    driver.get(url_copy)
    time.sleep(4)
    url = driver.page_source

    # Close the browser after copying the url for further analytics
    driver.quit()

    soup = BeautifulSoup(url, 'lxml')
    captures = soup.find_all('div', class_="match")

    # This line of code sorts the list of captures by date in ascending order from oldest to present.
    # The sorted() function takes a list of captures and sorts by the method called, in this case extract_date()
    sorted_captures = sorted(captures, key=extract_date)
    message = ""
    if not sorted_captures:
        # In other words, if no matches appear for dates then terminate the operation.
        pyautogui.hotkey('ctrl', 'w')
    else:

        for capture in sorted_captures:
            link_title = capture.find('h4').text.replace(' ', '')  # Removes raw code from HTML
            link = capture.h4.a
            date = capture.find('span', class_="crawl-date").text
            if link:
                # link_text = link.text.strip()
                link_href = link['href']
                message += f"""
Title: {link_title}    
Link: {link_href}
Date: {date}
"""
    return message


# Used to create folders for the evidence results, if folder input and path is blank then the method will create one.
def file_action():
    global folder_path, file_path

    try:
        folder_path = text_field1.get()

        file_path = text_field2.get()

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_paths = os.path.join(folder_path, f"{file_path}.txt")
        # Write the message to a .txt file
        with open(file_paths, "a") as file:
            file.write("")

        # print(f"\nFolder '{folder_path}' and file '{file_path}.txt' created successfully.")
        output_text.insert("end", f"\nFolder '{folder_path}' and file '{file_path}.txt' created successfully.")
        return folder_path, file_path

    except KeyboardInterrupt:
        print("Exiting upload action...")
        return


# Main bot process for automation
def run_analysis(folder_path=None, file_path=None):
    global default_folder, default_file
    toggle_hidden_text()

    if folder_path is None:
        folder_path = default_folder
    else:
        folder_path = text_field1.get()

    if file_path is None:
        file_path = default_file
    else:
        file_path = text_field3.get()

    # folder_path = text_field1.get()
    # file_path = text_field2.get()
    image_path = text_field3.get()
    image_path_replace = image_path.replace("/", "\\")

    if not image_path:
        output_text.insert("end", "Please provide a file path.\n")

    try:
        with open(image_path.replace("/", "\\"), "rb") as file:
            file.read()
            output_text.insert("end", "Image data uploaded successfully.\n")
    except FileNotFoundError as e:
        output_text.insert("end", "File not found.\n")
        return
    except Exception as e:
        output_text.insert("end", "Error while reading the file, please place correct filepath. {e}")
        return

    if selected_os.get() == "Windows":
        output_text.insert("end", "Conducting analysis...\n")

        time.sleep(5)
        pyautogui.press("win")
        pyautogui.typewrite("cmd")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.typewrite("start Firefox.exe https://tineye.com && exit")
        time.sleep(1.4)
        pyautogui.press("enter")

        time.sleep(3)
        upload_button = pyautogui.locateOnScreen("Button1.png", confidence=0.7)
        pyautogui.moveTo(upload_button, duration=0.3)
        pyautogui.leftClick()
        time.sleep(1)
        pyautogui.typewrite(image_path_replace)
        time.sleep(1.5)
        pyautogui.press("enter")
        time.sleep(7)

        evidence_message = tiny_collect()  # Define tiny_collect() function

        if evidence_message.strip():
            file_paths = os.path.join(folder_path, f"{file_path}.txt")
            with open(file_paths, "a") as file:
                file.write(evidence_message)

            output_text.insert("end", "\nEvidence saved.")
        else:
            output_text.insert("end", "\nCould not find any matches.")

        time.sleep(2)
        # Close the browser
        pyautogui.hotkey('ctrl', 'w')

    elif selected_os.get() == "Mac":
        output_text.insert("end", "Conducting analysis...\n")
    else:
        output_text.insert("end", "Please select either Windows or Mac to run Analysis.\n")


# Closes the program
def cancel():
    window.destroy()


# Main GUI for HarvestR using customtkinter and tkinter
window = ctk.CTk()

window.title("HarvestR")
window.after(201, lambda: window.iconbitmap('Icon40.ico'))
window.geometry('840x740')
window.resizable(False, False)

# Header Label
label = ctk.CTkLabel(window,
                     text='HarvestR / DNS OSINT Tool (versions 1.01)',
                     font=("Arial", 14, "bold"),
                     text_color='black',
                     fg_color='orange')
label.pack(fill="x")

s = ttk.Style()
s.theme_use('default')
s.configure('TNotebook.Tab', background="#FFA500", font=('Arial', 10, 'bold'))
s.configure('TNotebook', background='#242424', foreground='#242424', bordercolor='#242424')
s.map("TNotebook", background=[("selected", "#FFA500")])

# Create Tabview
my_tab = ttk.Notebook(window, width=1045, height=860)
my_tab.pack()

# Define the tab_1 and tab_2 frames
tab_1 = Frame(my_tab, bg="#242424")
tab_2 = Frame(my_tab, bg="#242424")
tab_3 = Frame(my_tab, bg="#242424")

tab_1.pack(fill="both", expand=True)

# Add the tab frames to the notebook
my_tab.add(tab_1, text="Image-Recon")
my_tab.add(tab_2, text="DNS")
my_tab.add(tab_3, text="Social Scrapper")

# Label 1
label1 = ctk.CTkLabel(tab_1,
                      text='File Creation / Evidence Location',
                      font=("Arial", 14, "bold"),
                      text_color='white')
label1.place(x=30, y=20)

# Container 1
container1 = ctk.CTkFrame(master=tab_1,
                          width=780,
                          height=120,
                          fg_color="light gray",
                          corner_radius=20)
container1.pack(pady=(60, 0))

# Create labels within Container 1
label_folder_name = ctk.CTkLabel(master=container1,
                                 text="Folder Name:",
                                 font=("Arial", 14, "bold"),
                                 text_color='black')
label_folder_name.place(x=80, y=20)

# Create labels within container 1
label_file_name = ctk.CTkLabel(master=container1,
                               text="File Name:",
                               font=("Arial", 14, "bold"),
                               text_color='black')
label_file_name.place(x=99, y=60)

# Text field 1 (Folder Name)
text_field1 = ctk.CTkEntry(master=container1,
                           width=450,
                           font=("Arial", 12),
                           fg_color="white",
                           text_color='black',
                           placeholder_text="Default Evidence")
text_field1.place(x=190, y=20)

# Text field 2 (File Name)
text_field2 = ctk.CTkEntry(master=container1,
                           width=450,
                           font=("Arial", 12),
                           fg_color="white",
                           text_color='black',
                           placeholder_text="Default Image Forensic Report")
text_field2.place(x=190, y=60)

# Button 1: Browse for Folder Name
button1 = ctk.CTkButton(master=container1,
                        text="browse",
                        font=("Arial", 12, "bold"),
                        fg_color="white",
                        text_color="black",
                        hover_color='orange',
                        width=110,
                        command=lambda: browse(text_field1))
button1.place(x=650, y=20)

# Button 2: Browse for File Name
button2 = ctk.CTkButton(master=container1,
                        text="browse",
                        font=("Arial", 12, "bold"),
                        fg_color="white",
                        text_color="black",
                        hover_color='orange',
                        width=110,
                        command=lambda: browse(text_field2))
button2.place(x=650, y=60)

# Label 3
label3 = ctk.CTkLabel(tab_1,
                      text='Upload / Search Image',
                      font=("Arial", 14, "bold"),
                      text_color='white')
label3.place(x=30, y=200)

# Container 2
container2 = ctk.CTkFrame(master=tab_1,
                          width=780,
                          height=240,
                          fg_color="light gray",
                          corner_radius=20)
container2.pack(pady=(60, 0))

# Create label within Container 2
label_Path_to_Image = ctk.CTkLabel(master=container2,
                                   text="File Path to Image:",
                                   font=("Arial", 14, "bold"),
                                   text_color='black')
label_Path_to_Image.place(x=42, y=20)

# Text field 3 (File Path to Image)
text_field3 = ctk.CTkEntry(master=container2,
                           width=450,
                           font=("Arial", 12),
                           fg_color="white",
                           text_color='black',
                           placeholder_text="Exact File Path")
text_field3.place(x=190, y=20)

# Button 3: Browse for Folder Name
button3 = ctk.CTkButton(master=container2,
                        text="browse",
                        font=("Arial", 12, "bold"),
                        fg_color="white",
                        text_color="black",
                        hover_color='orange',
                        width=110,
                        command=lambda: browse(text_field3))
button3.place(x=650, y=20)

label_Select_OS = ctk.CTkLabel(master=container2,
                               text="Select OS:",
                               font=("Arial", 14, "bold"),
                               text_color='black')
label_Select_OS.place(x=99, y=70)

# Sets the value
selected_os = ctk.StringVar(value="other")

# Radio button 1: Windows
radio_button1 = ctk.CTkRadioButton(master=container2,
                                   text="Windows",
                                   font=("Arial", 14, "bold"),
                                   text_color="black",
                                   hover_color="orange",
                                   value="Windows",
                                   variable=selected_os)
radio_button1.place(x=190, y=70)

# Radio button 2: Mac
radio_button2 = ctk.CTkRadioButton(master=container2,
                                   text="Mac",
                                   font=("Arial", 14, "bold"),
                                   text_color="black",
                                   hover_color="orange",
                                   value="Mac",
                                   variable=selected_os)
radio_button2.place(x=300, y=70)

# Button 4: Run Analysis
button4 = ctk.CTkButton(master=container2,
                        text="Run Analysis",
                        font=("Arial", 14, "bold"),
                        fg_color="white",
                        bg_color='light gray',
                        text_color="black",
                        hover_color="orange",
                        width=240,
                        height=35,
                        command=run_analysis)
button4.place(x=520, y=190)

# Button 5: Cancel
button5 = ctk.CTkButton(master=container2,
                        text="Cancel",
                        font=("Arial", 14, "bold"),
                        fg_color="white",
                        bg_color='light gray',
                        text_color="black",
                        hover_color="orange",
                        width=240,
                        height=35,
                        command=cancel)
button5.place(x=20, y=190)

output_text = ctk.CTkTextbox(master=tab_1,
                             width=780,
                             height=110,
                             font=("Arial", 12),
                             text_color="white",
                             border_color="gray",
                             wrap="word")
output_text.pack(pady=20)


# ----------------------------------------------------------------------------------------------------- End of First Tab
# -------------------------------------------------------------------------------------- Beginning of DNS: Credit Andrew

# Converts the tag elements into strings
def contentToText(tableContent, tableText):
    tableLength = len(tableContent)
    for i in range(tableLength):
        tableText.insert(i, tableContent[i].text.replace('\n', ' '))


# Converts tag elements into strings for each table
def setTableText():
    contentToText(dbIP_tableContents, dbIP_tableContents_text)
    contentToText(ipgeolocation_tableContents, ipgeolocation_tableContents_text)
    contentToText(ip2location_tableContents, ip2location_tableContents_text)
    contentToText(geolite2_tableContents, geolite2_tableContents_text)
    contentToText(ipinfoio_tableContents, ipinfoio_tableContents_text)


# Gets the element name only from table
def getElementName(elementName):
    element = int(elementName)

    match element:
        case 0:
            elementName = dbIP_tableContents[element].text.strip()[:10]  # IP
        case 1:
            elementName = dbIP_tableContents[element].text.strip()[:9]  # Host Name
        case 2:
            elementName = dbIP_tableContents[element].text.strip()[:8]  # IP Range
        case 3:
            elementName = dbIP_tableContents[element].text.strip()[:3]  # ISP
        case 4:
            elementName = dbIP_tableContents[element].text.strip()[:12]  # Organization
        case 5:
            elementName = dbIP_tableContents[element].text.strip()[:7]  # Country
        case 6:
            elementName = dbIP_tableContents[element].text.strip()[:6]  # Region
        case 7:
            elementName = dbIP_tableContents[element].text.strip()[:4]  # City
        case 8:
            elementName = dbIP_tableContents[element].text.strip()[:9]  # Time Zone
        case 9:
            elementName = dbIP_tableContents[element].text.strip()[:10]  # Local Time
        case 10:
            elementName = dbIP_tableContents[element].text.strip()[:11]  # Postal Code

    return elementName


def contentFormat(table, element, elementLength):
    updatedContent = ''
    contentLength = len(table[element].text.strip())

    if contentLength + 1 == elementLength:
        return updatedContent
    else:
        match element:
            case 2:  # "3" IP Range
                updatedContent = table[element].text.strip()[elementLength + 1:-6] + ' ' + table[element].text.strip()[
                                                                                           contentLength - 4:]
            case 5:  # "6" Country
                updatedContent = table[element].text.strip()[elementLength + 2:-5] + ' ' + table[element].text.strip()[
                                                                                           contentLength - 4:]
            case 8:  # "9" Time Zone
                updatedContent = table[element].text.strip()[elementLength + 1:]
            case default:
                updatedContent = table[element].text.strip()[elementLength:]

    return updatedContent


# Print the format for printElements()
def printFormat(elementName, tableName, tableContent):
    # centering the format
    longestTableName = 29
    dashes = (longestTableName - len(tableName)) + 10

    # Main output print
    visual_box2.insert("end", f'%s\n%s{" %s" :->{dashes}}\n\n' % (elementName, tableName, tableContent))


# Format the content for printElements()
def contentFormat(table, element, elementLength):
    updatedContent = ''
    contentLength = len(table[element].text.strip())

    if contentLength + 1 == elementLength:
        return updatedContent
    else:
        match element:
            case 2:  # "3" IP Range
                updatedContent = table[element].text.strip()[elementLength + 1:-6] + ' ' + table[element].text.strip()[
                                                                                           contentLength - 4:]
            case 5:  # "6" Country
                updatedContent = table[element].text.strip()[elementLength + 2:-5] + ' ' + table[element].text.strip()[
                                                                                           contentLength - 4:]
            case 8:  # "9" Time Zone
                updatedContent = table[element].text.strip()[elementLength + 1:]
            case default:
                updatedContent = table[element].text.strip()[elementLength:]

    return updatedContent


# num arg, prints specific element from each table
def printElements(element):
    # Organize the table's name *readable*
    dbIP = dbIP_table.a.text.strip()[:5] + ' ' + dbIP_table.a.text.strip()[6:]
    ipgeolocation = ipgeolocation_table.a.text.strip()[:16] + ' ' + ipgeolocation_table.a.text.strip()[17:]
    ip2location = ip2location_table.a.text.strip()[:11] + ' ' + ip2location_table.a.text.strip()[12:]
    geolite2 = geolite2_table.a.text.strip()[:13] + ' ' + geolite2_table.a.text.strip()[14:]
    ipinfoio = ipinfoio_table.a.text.strip()[:9] + ' ' + ipinfoio_table.a.text.strip()[10:]

    # elementName's length for getting the content
    elementLength = len(getElementName(element)) + 1

    # Element content
    dbIP_Content = contentFormat(dbIP_tableContents, element, elementLength)
    ipgeolocation_Content = contentFormat(ipgeolocation_tableContents, element, elementLength)
    ip2location_Content = contentFormat(ip2location_tableContents, element, elementLength)
    geolite2_Content = contentFormat(geolite2_tableContents, element, elementLength)
    ipinfoio_Content = contentFormat(ipinfoio_tableContents, element, elementLength)

    # Print table name and elements related
    printFormat(getElementName(element), dbIP, dbIP_Content)
    printFormat(getElementName(element), ipgeolocation, ipgeolocation_Content)
    printFormat(getElementName(element), ip2location, ip2location_Content)
    printFormat(getElementName(element), geolite2, geolite2_Content)
    printFormat(getElementName(element), ipinfoio, ipinfoio_Content)


# Loop through table list, return string
def listToString(table):
    stringTable = ''
    tableLength = len(table)

    for i in range(tableLength):
        elementName = getElementName(i)
        elementContent = table[i][len(getElementName(i)) + 2:]

        longestElementName = 12
        dashes = (longestElementName - len(elementName)) + 10

        stringTable += f'  %s {" %s":->{dashes}}' % (elementName, elementContent) + '\n'

    stringTable += '\n\n'

    return stringTable


# Pass the text list to a single String
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


# Print the elements header ie IP, Host Name, etc
def listHeaders():
    headerTags = []
    for i in range(len(dbIP_tableContents)):
        headerTags.insert(i, dbIP_tableContents[i].td)
        visual_box2.insert("end", f'%2d. {headerTags[i].text}' % (i+1))


# Cases to select specific elements
def selectElement(value):
    visual_box2.delete(1.0, "end")

    # listHeaders()  # For display purposes
    choice = value

    match choice:
        case 'IP':
            choice = 1  # IP
            printElements(choice)
        case '2':
            choice = 2  # Host Name
            printElements(choice)
        case '3':
            choice = 3  # IP Range
            printElements(choice)
        case '4':
            choice = 4  # ISP
            printElements(choice)
        case '5':
            choice = 5  # Organization
            printElements(choice)
        case '6':
            choice = 6  # Country
            printElements(choice)
        case '7':
            choice = 7  # Region
            printElements(choice)
        case '8':
            choice = 8  # City
            printElements(choice)
        case '9':
            choice = 9  # Time Zone
            printElements(choice)
        case '10':
            choice = 10  # Local Time
            printElements(choice)
        case '11':
            choice = 11  # Postal Code
            printElements(choice)

    choice = my_combo.get()

    # Define mapping of choices to their corresponding indexes
    choice_mapping = {
        "IP": 1,
        "Host Name": 2,
        "ISP": 4,
        "Organization": 5,
        "Country": 6,
        "Region": 7,
        "City": 8,
        "Time Zone": 9,
        "Local Time": 10,
        "Postal code": 11
    }

    # Get the index corresponding to the selected choice
    choice_index = choice_mapping.get(choice)

    if choice_index is not None:
        # listHeaders()
        printElements(choice_index)
    else:
        visual_box2.insert("end", 'Could not display anything.')  # Default case


# Create text file and pass table info
def writeFile():
    tables = open("newFile.txt", 'w')
    tables.write(passList())
    tables.close()


# The link: had to put this here, not a fan
def domainNameLink():

    visual_box1.delete(1.0, "end")

    global dbIP_tableContents, ipgeolocation_tableContents, ip2location_tableContents, geolite2_tableContents
    global ipinfoio_tableContents
    global dbIP_tableContents_text, ipgeolocation_tableContents_text, ip2location_tableContents_text
    global geolite2_tableContents_text, ipinfoio_tableContents_text
    global dbIP_table, ipgeolocation_table, ip2location_table, geolite2_table, ipinfoio_table

    domainName = text_field4.get()

    pattern = r'\.(com|org|net|edu|gov|mil|int)$'
    match = re.search(pattern, domainName, re.IGNORECASE)

    if not match:
        visual_box1.insert("end", '\nNo information found. Please use URL extensions (.com, .org, etc).\n')
        visual_box2.insert("end", '\nNo information found. Please use URL extensions (.com, .org, etc).\n')
        return None

    siteName = 'https://check-host.net/ip-info?host='
    siteToken = '&csrf_token=4d2ba08a6cadb5a4bcc845de3d4b9a4ddbeba508'

    # option = my_combo.get()

    url = siteName + domainName + siteToken

    visual_box1.insert("end", domainName)
    visual_box1.insert("end", "\n\n")

    siteHtml = requests.get(url).text
    soup = BeautifulSoup(siteHtml, 'lxml')

    tables = soup.find('div', id='content2')

    dbIP_table = tables.find('div', id='ip_info-dbip')
    ipgeolocation_table = tables.find('div', id='ip_info-ipgeolocation')
    ip2location_table = tables.find('div', id='ip_info-ip2location')
    geolite2_table = tables.find('div', id='ip_info-geolite2')
    ipinfoio_table = tables.find('div', id='ip_info-ipinfoio')

    dbIP_tableContents = dbIP_table.find_all('tr')
    ipgeolocation_tableContents = ipgeolocation_table.find_all('tr')
    ip2location_tableContents = ip2location_table.find_all('tr')
    geolite2_tableContents = geolite2_table.find_all('tr')
    ipinfoio_tableContents = ipinfoio_table.find_all('tr')

    # Global list to collect the tables data for improving readability
    dbIP_tableContents_text = []
    ipgeolocation_tableContents_text = []
    ip2location_tableContents_text = []
    geolite2_tableContents_text = []
    ipinfoio_tableContents_text = []

    setTableText()

    visual_box1.insert("end", passList())  # Display the search


# Define image
bg = PhotoImage(file="DNSBackgroundLarge.png")

# Transparent color
window.wm_attributes('-transparentcolor', '#382276')

canvas = Canvas(tab_2, width=840, height=740, background='black', highlightthickness=0)

canvas.create_image(5, 0, image=bg, anchor=NW)
canvas.create_text(105, 50, text='DNS Lookup', fill="white", font=('Arial', 12, 'bold'))
canvas.create_text(105, 350, text='Table View ', fill="white", font=('Arial', 12, 'bold'))
canvas.create_text(720, 350, text='Element View: ', fill="white", font=('Arial', 12, 'bold'))
canvas.pack(fill="both", expand=True)

# Tab Container 2
tab_2_container = ctk.CTkFrame(master=tab_2,
                               width=770,
                               height=180,
                               fg_color="#2D3C4C",
                               bg_color="#000001",
                               corner_radius=20)
tab_2_container.place(relx=0.04, rely=0.1, anchor="nw")

# Used for transparency
# pywinstyles.set_opacity(tab_2_container, color="#000001")

# Label for Domain
tab2_label = ctk.CTkLabel(tab_2_container,
                          text='Domain: ',
                          font=("Arial", 14, "bold"),
                          text_color='white',
                          bg_color="#2D3C4C")
tab2_label.place(relx=0.1, rely=0.3, anchor="nw")

# Text field 4 (Enter Domain Name)
text_field4 = ctk.CTkEntry(master=tab_2_container,
                           width=450,
                           font=("Arial", 12),
                           fg_color="white",
                           text_color='black',
                           placeholder_text="Enter Domain Name")
text_field4.place(relx=0.2, rely=0.3, anchor="nw")

# Button 5: Run DNS Search
button5 = ctk.CTkButton(master=tab_2_container,
                        text="Search",
                        font=("Arial", 12, "bold"),
                        fg_color="white",
                        bg_color='#2D3C4C',
                        text_color="black",
                        hover_color="light blue",
                        width=110,
                        command=lambda: domainNameLink())
button5.place(relx=0.42, rely=0.55, anchor="nw")

# Button 6: Run DNS Search
button6 = ctk.CTkButton(master=tab_2_container,
                        text="Save",
                        font=("Arial", 12, "bold"),
                        fg_color="white",
                        bg_color='#2D3C4C',
                        text_color="black",
                        hover_color="light blue",
                        width=110,
                        command=lambda: writeFile())
button6.place(relx=0.42, rely=0.75, anchor="nw")

view = ["IP",
        "Host Name",
        "ISP",
        "Organization",
        "Country",
        "Region",
        "City",
        "Time Zone",
        "Local Time",
        "Postal code"]


# Dropdown for view 2
my_combo = ctk.CTkComboBox(tab_2,
                           values=view,
                           width=170,
                           dropdown_fg_color="white",
                           dropdown_text_color="black",
                           dropdown_hover_color="light gray",
                           fg_color="white",
                           text_color="black",
                           command=selectElement)
my_combo.place(relx=0.76, rely=0.39, anchor="nw")
my_combo.set('Select view type')

# Visual display 1
visual_box1 = ctk.CTkTextbox(master=tab_2,
                             width=370,
                             height=360,
                             font=("Arial", 12),
                             text_color="black",
                             fg_color="white",
                             wrap="word")
visual_box1.place(relx=0.04, rely=0.45, anchor="nw")

# Visual display 2
visual_box2 = ctk.CTkTextbox(master=tab_2,
                             width=370,
                             height=360,
                             font=("Arial", 12),
                             text_color="black",
                             fg_color="white",
                             wrap="word")
visual_box2.place(relx=0.52, rely=0.45, anchor="nw")

window.mainloop()
