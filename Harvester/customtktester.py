import customtkinter
import pywinstyles
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
import customtkinter as ctk


# These variables are global
hidden_text_id = None
default_folder = "Evidence"
default_file = "Image Forensic Report"
folder_path = None
file_path = None


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


def browse(text_field):
    # Function for browsing file path

    selected_path = filedialog.askdirectory() if text_field == text_field1 else filedialog.askopenfilename()
    text_field.delete(0, "end")
    text_field.insert(0, selected_path)


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


def cancel():
    window.destroy()


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

# Define image
bg = PhotoImage(file="DNSBackgroundLarge.png")

# Label 1
label1 = ctk.CTkLabel(tab_1,
                      text='File Creation / Evidence Location',
                      font=("Arial", 14, "bold"),
                      text_color='white',
                      )
label1.place(x=30, y=20)

# Container 1
container1 = ctk.CTkFrame(master=tab_1,
                          width=780,
                          height=120,
                          fg_color="light gray",
                          corner_radius=20  # Adjust the corner radius as needed
                          )
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
                      text_color='white',
                      )
label3.place(x=30, y=200)

# Container 2
container2 = ctk.CTkFrame(master=tab_1,
                          width=780,
                          height=240,
                          fg_color="light gray",
                          corner_radius=20  # Adjust the corner radius as needed
                          )
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
                        command=cancel
                        )
button5.place(x=20, y=190)

output_text = ctk.CTkTextbox(master=tab_1,
                             width=780,
                             height=110,
                             font=("Arial", 12),
                             text_color="white",
                             border_color="gray",
                             wrap="word")
output_text.pack(pady=20)

# --------------------------------------------------------------- End of First Tab

# Transparent color
window.wm_attributes('-transparentcolor', '#382276')

canvas = Canvas(tab_2, width=840, height=740, background='black', highlightthickness=0)

canvas.create_image(5, 0, image=bg, anchor=NW)
canvas.create_text(105, 50, text='DNS Lookup', fill="white", font=('Arial', 12, 'bold'))
canvas.create_text(260, 350, text='View: ', fill="white", font=('Arial', 12, 'bold'))
canvas.create_text(760, 350, text='View: ', fill="white", font=('Arial', 12, 'bold'))
canvas.pack(fill="both", expand=True)

# Tab Container 2
tab_2_container = ctk.CTkFrame(master=tab_2,
                               width=770,
                               height=180,
                               fg_color="#2D3C4C",
                               bg_color="#000001",
                               corner_radius=20  # Adjust the corner radius as needed
                               )
tab_2_container.place(relx=0.04, rely=0.1, anchor="nw")

# Used for transparency
pywinstyles.set_opacity(tab_2_container, color="#000001")

# Label for Domain
tab2_label = ctk.CTkLabel(tab_2_container,
                          text='Domain: ',
                          font=("Arial", 14, "bold"),
                          text_color='white',
                          bg_color="#2D3C4C"
                          )
tab2_label.place(relx=0.1, rely=0.2, anchor="nw")

# Text field 4 (Enter Domain Name)
text_field4 = ctk.CTkEntry(master=tab_2_container,
                           width=400,
                           font=("Arial", 12),
                           fg_color="white",
                           text_color='black',
                           placeholder_text="Enter Domain Name")
text_field4.place(relx=0.2, rely=0.2, anchor="nw")

# Label for Domain
tab2_label2 = ctk.CTkLabel(tab_2_container,
                           text='Element: ',
                           font=("Arial", 14, "bold"),
                           text_color='white',
                           bg_color="#2D3C4C"
                           )
tab2_label2.place(relx=0.092, rely=0.5, anchor="nw")


def element_picker(choice):
    print()


elements = ["Select Element", "Tables"]
# Dropdown for elements
my_combo = customtkinter.CTkComboBox(tab_2_container,
                                     values=elements,
                                     width=170,
                                     dropdown_fg_color="white",
                                     dropdown_text_color="black",
                                     dropdown_hover_color="light gray",
                                     fg_color="white",
                                     text_color="black",
                                     command=element_picker
                                     )
my_combo.place(relx=0.2, rely=0.5, anchor="nw")
my_combo.set('Select Element')

view = ["IP", "Host Name", "ISP", "Organization", "Country", "Region", "City", "Time Zone", "Local Time", "Postal code"]

# Dropdown for view 1
my_combo2 = customtkinter.CTkComboBox(tab_2,
                                      values=view,
                                      width=170,
                                      dropdown_fg_color="white",
                                      dropdown_text_color="black",
                                      dropdown_hover_color="light gray",
                                      fg_color="white",
                                      text_color="black",
                                      command=element_picker
                                      )
my_combo2.place(relx=0.28, rely=0.39, anchor="nw")
my_combo2.set('Select view type')

# Dropdown for view 2
my_combo3 = customtkinter.CTkComboBox(tab_2,
                                      values=view,
                                      width=170,
                                      dropdown_fg_color="white",
                                      dropdown_text_color="black",
                                      dropdown_hover_color="light gray",
                                      fg_color="white",
                                      text_color="black",
                                      command=element_picker
                                      )
my_combo3.place(relx=0.76, rely=0.39, anchor="nw")
my_combo3.set('Select view type')

# Visual display 1
Visual_box1 = ctk.CTkTextbox(master=tab_2,
                             width=370,
                             height=360,
                             font=("Arial", 12),
                             text_color="black",
                             fg_color="white",
                             wrap="word")
Visual_box1.place(relx=0.04, rely=0.45, anchor="nw")

# Visual display 2
Visual_box2 = ctk.CTkTextbox(master=tab_2,
                             width=370,
                             height=360,
                             font=("Arial", 12),
                             text_color="black",
                             fg_color="white",
                             wrap="word")
Visual_box2.place(relx=0.52, rely=0.45, anchor="nw")

window.mainloop()
