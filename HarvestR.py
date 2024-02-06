from PIL import Image
import pyautogui
import time

def tune_action():
    print("\nTune menu item selected")

def upload_action():
    filepath = input("Please enter filepath to your Image (Without Quotations): ")

    try:
        with open(filepath, "rb") as file:
            image_data = file.read()
        print("Image data uploaded successfully")

    except FileNotFoundError:
        print(f"File not found: {filepath}")

    print("Conducting analysis...")

    time.sleep(5)
    pyautogui.press("win")
    pyautogui.typewrite("cmd")
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.typewrite("start Firefox.exe https://tineye.com && exit")
    pyautogui.press("enter")

    #Old Method of searching
    # time.sleep(5)
    # x, y = pyautogui.locateCenterOnScreen("LittleFox.png", confidence=0.8)
    #
    # pyautogui.moveTo(x, y, duration=0.3)
    # pyautogui.doubleClick()

    time.sleep(3)
    upload_button = pyautogui.locateOnScreen("Button1.png", confidence=0.7)
    pyautogui.moveTo(upload_button, duration=0.3)
    pyautogui.leftClick()
    time.sleep(1)
    pyautogui.typewrite(filepath)
    pyautogui.press("enter")

def main_menu():
    while True:
        print("\n=== HarvestR Main Menu ===")
        print("""\nProcedures:
Please insure that there are no windows or obstructions in the view of your desktop before
running the tool. If you dont the tool will break :').
        """)
        print("1. Tune Search")
        print("2. Upload Image and Search Image")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            tune_action()
        elif choice == "2":
            upload_action()
        elif choice == "0":
            print("Exiting HarvestR. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()
