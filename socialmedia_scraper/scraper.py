   
import pyautogui
import webbrowser
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def instagram(name):
    
    
      
    
    url = 'https://www.instagram.com/' 
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(6)
    pyautogui.click(991,539)
    time.sleep(3)
    pyautogui.typewrite("kjman11555")
    pyautogui.press('tab')
    pyautogui.typewrite("Ilovegod1234")
    pyautogui.press("enter")
    time.sleep(4)
    urls=name 
    driver.get(urls)
    


   

    time.sleep(10)
    try:
        post_element = driver.find_element('css selector', 'li:nth-child(1) span.x1vvkbs')
        follower_element = driver.find_element('css selector', 'li:nth-child(2) span.x1vvkbs')
        following_element = driver.find_element('css selector', 'li:nth-child(3) span.x1vvkbs')
        bio = driver.find_element('class name', 'x7a106z')
        mimi_story = driver.find_element('class name', '_aap0')

        # Extract the text from the elements    
        bio_content = bio.text
        post_count = post_element.text
        follower_count = follower_element.text
        following_count = following_element.text
        story_content = mimi_story.text

        # Print the counts
        print("Post count:", post_count, "\n")
        print("Follower count:", follower_count, "\n")
        print("Following count:", following_count, "\n")
        print("bio:", bio_content, "\n")
        print("stories:", story_content, "\n")
    except TimeoutException:
        print("Some information could not be found:", e)

        

def linked(link):
   driver = webdriver.Chrome()


   url = link
   driver.get(url)
   time.sleep(5)
   pyautogui.moveTo(1276,280)
   pyautogui.click()
   time.sleep(5)
   headline_element = driver.find_element("css selector", "h2.top-card-layout__headline")
   headline = headline_element.text.strip()

   # Extracting experience details
   experience_section = driver.find_element("css selector", "section[data-section='experience']")
   experience_text = experience_section.text.strip()

   # Extracting education details
   education_section = driver.find_element("css selector", "section[data-section='educationsDetails']")
   education_text = education_section.text.strip()

   # Extracting person's name
   name_element = driver.find_element("css selector", "h1.top-card-layout__title")
   name = name_element.text.strip()




    # Print the extracted information
   print("Name:", name)
   print("Headline:", headline)
   print("\nExperience Details:")
   print(experience_text)
   print("\nEducation Details:")
   print(education_text)
   driver.quit()


    
     
   
def main():
  

    running = True


    while running:
     choice = input("Enter '1' for Instagram search or '2' for LinkedIn search  or 3 for all (or type 'quit' to exit): ")

     if choice == '1':
        username = input("Please enter the person's Instagram username: ")
        if username.strip() == '' or username.lower() == 'quit':
            print("Exiting...")
            running = False
        else:
            ig_name = "https://www.instagram.com/" + username + "/"
            instagram(ig_name)
            running = False
     elif choice == '2':
        linkedin_link = input("Please enter the person's LinkedIn profile link: ")
        if linkedin_link.strip() == '' or linkedin_link.lower() == 'quit':
            print("Exiting...")
            running = False
        else:
            linked(linkedin_link)
            running = False
     elif choice.lower() == 'quit':
        print("Exiting...")
        running = False
     elif choice == '3':
        username = input("Please enter the person's Instagram username: ")
        linkedin_link = input("Please enter the person's LinkedIn profile link: ")
        if username.strip() == '' or linkedin_link.strip() == '' or username.lower() == 'quit' or linkedin_link.lower() == 'quit':
            print("Exiting...")
            running = False
        else:
            ig_name = "https://www.instagram.com/" + username + "/"
            instagram(ig_name)
            linked(linkedin_link)
            running = False
     elif choice.lower() == 'quit':
        print("Exiting...")
        running = False
     else:
        print("Invalid choice. Please enter '1' for Instagram search, '2' for LinkedIn search, '3' for both, or 'quit' to exit.")

    running = False
  

 
if __name__ == '__main__':

    main()  
