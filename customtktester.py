from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from tkinter import filedialog
import pyautogui
import time
import pyperclip
import re
import os
import customtkinter as ctk

window = ctk.CTk()

window.title("HarvestR")
window.after(201, lambda: window.iconbitmap('Icon40.ico'))
window.geometry('840x740')


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
        # In other words, if no matches appear for dates then return no matches found.
        print("Could not find any matches.")
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

        print(f"\nFolder '{folder_path}' and file '{file_path}.txt' created successfully.")
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
        return

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

        file_paths = os.path.join(folder_path, f"{file_path}.txt")
        with open(file_paths, "a") as file:
            file.write(evidence_message)

        output_text.insert("end", "Evidence saved.")

        time.sleep(2)
        # Close the browser
        pyautogui.hotkey('ctrl', 'w')

    elif selected_os.get() == "Mac":
        output_text.insert("end", "Conducting analysis...\n")
    else:
        output_text.insert("end", "Please select either Windows or Mac to run Analysis.\n")


def cancel():
    window.destroy()


# Header Label
label = ctk.CTkLabel(window,
                     text='HarvestR OSINT Image Recognition Tool (versions 1.01)',
                     font=("Arial", 14, "bold"),
                     text_color='black',
                     fg_color='orange')
label.pack(fill="x")

# Label 1
label1 = ctk.CTkLabel(window,
                      text='File Creation / Evidence Location',
                      font=("Arial", 14, "bold"),
                      text_color='white',
                      )
label1.place(x=30, y=90)

# Container 1
container1 = ctk.CTkFrame(master=window,
                          width=780,
                          height=120,
                          fg_color="light gray",
                          corner_radius=20  # Adjust the corner radius as needed
                          )
container1.pack(pady=(100, 0))

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
label3 = ctk.CTkLabel(window,
                      text='Upload / Search Image',
                      font=("Arial", 14, "bold"),
                      text_color='white',
                      )
label3.place(x=30, y=270)

# Container 2
container2 = ctk.CTkFrame(master=window,
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

output_text = ctk.CTkTextbox(master=window,
                             width=780,
                             height=110,
                             font=("Arial", 12),
                             text_color="white",
                             border_color="gray",
                             wrap="word")
output_text.pack(pady=20)


window.mainloop()
