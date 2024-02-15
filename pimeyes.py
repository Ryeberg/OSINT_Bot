import pyautogui
import time

time.sleep(3)

pyautogui.hotkey('ctrl', 'l')
pyautogui.typewrite("pimeyes.com/en")
pyautogui.press("enter")

time.sleep(3)

upload_button= pyautogui.locateOnScreen('uploadButton.png', confidence= .7)
pyautogui.moveTo(upload_button, duration= 0.4)
pyautogui.leftClick()
upload_next= pyautogui.locateOnScreen('uploadNext.png', confidence= .7)
pyautogui.moveTo(upload_next, duration= 0.4)
pyautogui.leftClick()
