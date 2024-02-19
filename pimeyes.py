import pyautogui
from PIL import Image
import time

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
