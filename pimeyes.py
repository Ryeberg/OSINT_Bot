import pyautogui
from PIL import Image
import time
from cryptography.fernet import fernet

time.sleep(3)

pyautogui.hotkey('ctrl', 'l')
pyautogui.typewrite("pimeyes.com")
pyautogui.press("enter")

time.sleep(2)

upload_Button=pyautogui.locateOnScreen("uploadButton.png", confidence= .5)
pyautogui.moveTo(upload_Button, duration= 0.4)
pyautogui.leftClick()

upload_Next=pyautogui.locateOnScreen("uploadNext.png", confidence= .5)
pyautogui.moveTo(upload_Next, duration= 0.4)
pyautogui.leftClick()

time.sleep(1)
pyautogui.typewrite("peyton")
pyautogui.press("enter")

time.sleep(5)

#searchOption=pyautogui.locateOnScreen("safeSearch.png", confidence= .5)
#pyautogui.moveTo(searchOption, duration= 0.4)
#pyautogui.leftClick()

firstCheck=pyautogui.locateOnScreen("yearsAge.png", confidence= .5)
pyautogui.moveTo(firstCheck, duration= 0.4)
pyautogui.leftClick()

secondCheck=pyautogui.locateOnScreen("termsService.png", confidence= .5)
pyautogui.moveTo(secondCheck, duration= 0.4)
pyautogui.leftClick()

thirdCheck=pyautogui.locateOnScreen("privacyPolicy.png", confidence= .5)
pyautogui.moveTo(thirdCheck, duration= 0.4)
pyautogui.leftClick()
pyautogui.leftClick()

time.sleep(2)
screeshot = pyautogui.screenshot()
screeshot.save("otherLocations.png")
print("screenshot taken")

def generate_key():
    return Fernet.generate_key()  

def save_key(key, filename="secret.key"):
    with open(filename, "wb") as key_file:
        key_file.write(key)

def load_key(filename="secret.key"):  
    return open(filename, "rb").read()

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

if __name__ == "__main__":
    # Proper indentation
    key = generate_key()
    save_key(key)

    key = load_key()

    original_message = "Sensitive data here"
    encrypted_message = encrypt_message(original_message, key) 
    print(f"Encrypted: {encrypted_message}")  # Corrected variable reference

    decrypted_message = decrypt_message(encrypted_message, key)  
    print(f"Decrypted: {decrypted_message}")
