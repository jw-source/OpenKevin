from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

from selenium.webdriver import ActionChains

options = webdriver.FirefoxOptions()
#options.set_preference('profile', "C:\\Users\\Kenny\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\50xcwu7x.school-1632326509667")

driver = webdriver.Firefox(options=options)
driver.get("https://replit.com/join/hjfnvykdup-kennethkouge")

elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "username-:r0:")))

driver.find_element(By.ID, "username-:r0:").click()
driver.find_element(By.ID, "username-:r0:").send_keys(os.environ['REPLIT_EML'])
driver.find_element(By.ID, "password-:r6:").click()
driver.find_element(By.ID, "password-:r6:").send_keys(os.environ['REPLIT_PWD'])
driver.find_element(By.XPATH, "//button[span[text()='Log In']]").click()

def find_ai_box():
    elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(text(), 'Type message…')]")))
    return elements[0]

def contains_copies():
    copy = driver.find_element(By.XPATH, "//button[div[span[span[contains(text(), 'Copy')]]]]")
    return copy is not None

def get_latest_copy():
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[div[span[span[contains(text(), 'Copy')]]]]")))
    copy_btns = driver.find_elements(By.XPATH, "//button[div[span[span[contains(text(), 'Copy')]]]]")
    return copy_btns[-1]

def paste_into(filename="main.c"):
    fileelem = driver.find_element(By.XPATH, f"//div[@title='{filename}']")
    fileelem.click()
    code_box = elements[0]
    ActionChains(driver).move_to_element(code_box).click(code_box).key_down(Keys.CONTROL).send_keys("A").key_up(Keys.CONTROL)\
    .key_down(Keys.CONTROL).send_keys("V").key_up(Keys.CONTROL).perform()

demo_prompt = 'Please replace all instances of scanf with the more secure sscanf. Please give the full code of the file, in a markdown box.'
import time

def do_full_process(filename="main.c", prompt=demo_prompt):
    ai_box = find_ai_box()

    old_copy = None
    if contains_copies():
        old_copy = get_latest_copy()
    
    # send text into AI box
    ActionChains(driver).move_to_element(ai_box).click(ai_box).send_keys(filename + prompt).send_keys(Keys.RETURN).perform()

    print('old copy is:', old_copy)
    # copy text from latest copy
    while get_latest_copy() == old_copy:
        print('searching for new copy')
        time.sleep(0.5)
    copy_btn = get_latest_copy()
    copy_btn.click()

    # paste into relevant file
    paste_into(filename)
