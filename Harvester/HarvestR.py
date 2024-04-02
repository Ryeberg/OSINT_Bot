from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import pyautogui
import time
import pyperclip
import re
import os

def extract_date(capture):
    date_str = capture.find('span', class_="crawl-date").text
    # re.search()searches for the first occurrence of a pattern within a string.
    # (\w+ \d+ \d+) is a pattern that searches a word first then two integers like a date: May, 13, 1994
    match = re.search(r'(\w+ \d+, \d+)', date_str)
    if match:
        # group(0) is referring to the entire matched substring
        date_str = match.group(0)
        # datetime.strptime converts the date string to a datetime object for sorting
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

    if not sorted_captures:
        # In other words, if no matches appear for dates then return no matches found.
        print("Could not find any matches.")
    else:
        message = ""
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
    global folder_name, file_name

    try:
        folder_name = input("Enter the name of the folder to save the evidence: ")
        if folder_name.lower() == "exit":
            print("Exiting upload action...")
            return None, None

        file_name = input("Enter the name of the file to save the evidence (without extensions): ")
        if file_name.lower() == "exit":
            print("Exiting upload action...")
            return None, None

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, f"{file_name}.txt")
        # Write the message to a .txt file
        with open(file_path, "a") as file:
            file.write("")

        print(f"\nFolder '{folder_name}' and file '{file_name}.txt' created successfully.")
        return folder_name, file_name

    except KeyboardInterrupt:
        print("Exiting upload action...")
        return


# These variables are global
default_folder = "Evidence"
default_file = "Image Forensic Report"
folder_name = None
file_name = None


def upload_action(folder_name=None, file_name=None):
    global default_folder, default_file

    if folder_name is None:
        folder_name = default_folder
    if file_name is None:
        file_name = default_file

    while True:
        filepath = input("Please enter filepath to your Image: ").replace('"', '')

        if filepath.lower() == "exit":
            print("Exiting upload action...")
            return

        try:
            with open(filepath, "rb") as file:
                file.read()
                print("Image data uploaded successfully")
                break
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"Error while reading the file, please place correct filepath. {e}")

    while True:
        os_input = input("Please select your OS (Windows / Mac) or type (exit) to go back to main menu: ").lower()
        print(f"You have selected {os_input}")

        if os_input == "windows":
            print("Conducting analysis...")

            time.sleep(5)
            pyautogui.press("win")
            pyautogui.typewrite("cmd")
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.typewrite("start Firefox.exe https://tineye.com && exit")
            time.sleep(1.4)
            pyautogui.press("enter")

            # Old Method of searching
            # time.sleep(5)
            # x, y = pyautogui.locateCenterOnScreen("LittleFox.png", confidence=0.8)

            # pyautogui.moveTo(x, y, duration=0.3)
            # pyautogui.doubleClick()

            time.sleep(3)
            # Uses Button1.png to recognize the same image and click on it
            upload_button = pyautogui.locateOnScreen("Button1.png", confidence=0.7)
            pyautogui.moveTo(upload_button, duration=0.3)
            pyautogui.leftClick()
            time.sleep(1)
            pyautogui.typewrite(filepath)
            time.sleep(1.5)
            pyautogui.press("enter")
            time.sleep(7)
            # Save all info collected into evidence_message to write to file
            evidence_message = tiny_collect()

            file_path = os.path.join(folder_name, f"{file_name}.txt")
            with open(file_path, "a") as file:
                file.write(evidence_message)

            print(f"Evidence saved to {file_path}")

            time.sleep(1)
            # Close the browser
            pyautogui.hotkey('ctrl', 'w')

            # pyautogui.hotkey('ctrl', 't')
            # pyautogui.typewrite("https://Google.com")
            # pyautogui.press("enter")
            break

        elif os_input == "mac":
            print("Conducting analysis...")
        elif os_input == "exit":
            break
        else:
            print("Wrong input. Please select either Windows or Mac.")


def main_menu():
    global folder_name, file_name

    while True:
        print("\n=== HarvestR Main Menu ===")
        print("""\nProcedures:
Please insure that there are no windows or obstructions in the view of your desktop before
running the tool. If you dont the tool will break :'). Type "exit" to return to the main menu.
        """)
        print("1. File Creation and Evidence Location")
        print("2. Upload Image and Search Image")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            folder_name, file_name = file_action()
        elif choice == "2":
            upload_action(folder_name, file_name)
        elif choice == "exit":
            print("Exiting HarvestR. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main_menu()
