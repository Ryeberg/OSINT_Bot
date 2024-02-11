from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pyautogui
import time
import pyperclip
import re

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
    pyautogui.hotkey('ctrl', 'l')  # This is to select the url
    pyautogui.hotkey('ctrl', 'c')

    # pyperclip is a libray that allows you to copy to a clipboard through python
    url_copy = pyperclip.paste()

    driver = webdriver.Firefox()  # Future code will involve multiple browsers
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
        for capture in sorted_captures:
            link_title = capture.find('h4').text.replace(' ', '')  # Removes raw code from HTML
            link = capture.h4.a
            date = capture.find('span', class_="crawl-date").text
            if link:
                link_text = link.text.strip()
                link_href = link['href']
                print(f"""
Title: {link_title}    
Link: {link_href}
Date: {date}
""")


def tune_action():
    print("\nTune menu item selected")

def upload_action():

    while True:
        filepath = input("Please enter filepath to your Image: ").replace('"','')

        try:
            with open(filepath, "rb") as file:

                image_data = file.read()
                print("Image data uploaded successfully")
                break
        except FileNotFoundError as e:
            print(f"File not found: {filepath}")
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
            upload_button = pyautogui.locateOnScreen("Button1.png", confidence=0.7)
            pyautogui.moveTo(upload_button, duration=0.3)
            pyautogui.leftClick()
            time.sleep(1)
            pyautogui.typewrite(filepath)
            time.sleep(1.5)
            pyautogui.press("enter")

            time.sleep(10)
            tiny_collect()

            time.sleep(1)
            pyautogui.hotkey('ctrl', 't')
            pyautogui.typewrite("https://Google.com")
            pyautogui.press("enter")


            break


        elif os_input == "mac":
            print("Conducting analysis...")
        elif os_input == "exit":
            break
        else:
            print("Wrong input. Please select either Windows or Mac.")

def main_menu():
    while True:
        print("\n=== HarvestR Main Menu ===")
        print("""\nProcedures:
Please insure that there are no windows or obstructions in the view of your desktop before
running the tool. If you dont the tool will break :'). Type "exit" to stop the program.
        """)
        print("1. Tune Search")
        print("2. Upload Image and Search Image")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            tune_action()
        elif choice == "2":
            upload_action()
        elif choice == "exit":
            print("Exiting HarvestR. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()
