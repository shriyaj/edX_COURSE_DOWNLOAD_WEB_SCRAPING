'''
Created on 01-Sep-2019

@author: Shriya
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import urllib.request
from locators import *
from locators2 import *
from test.test_largefile import size


def driver_init():
    driver = webdriver.Chrome('C:\\Users\\Shriya\\Downloads\\chromedriver.exe')
    return(driver)

def sign_in(driver):
    delay = 60 # seconds
    try:
        sign_in_btn = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, SIGN_IN_BUTTON)))
        print('Sign in button found')
        sign_in_btn.click()
    except TimeoutException:
        print("Loading took too much time!")
        exit()
#     sign_in_btn = driver.find_element_by_xpath(SIGN_IN_BUTTON)
      

def fb_sign_in(driver):
    fb_sign_in_btn = driver.find_element_by_xpath(FACEBOOK_SIGN_IN_BUTTON)
    print('Facebook Sign in button found')
    fb_sign_in_btn.click()
    
    driver.find_element_by_xpath(FACEBOOK_EMAIL_TEXTBOX).send_keys('Provide email ID here')
    driver.find_element_by_xpath(FACEBOOK_PASSWORD_TEXTBOX).send_keys('Provide corresponding password')
    login_btn = driver.find_element_by_xpath(FACEBOOK_LOGIN_BUTTON)
    login_btn.click()
    


def get_file_size(url):
    d = urllib.request.urlopen(url)
    return(d.info()['Content-Length'])

def file_name_bad_chars_remove(filename):
    for char in list('();,.<>:"/\|?*'):
        filename = filename.replace(char,'')
#     if len(filename) > 50:
#         filename = filename[:50]
    
    return(filename)
    
def get_video_url(driver):
    try:
        video_el = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, DOWNLOAD_VIDEO_BUTTON)))
#         video_el = driver.find_element_by_xpath(DOWNLOAD_VIDEO_BUTTON)
        video_url = video_el.get_attribute('href')
        return(video_url)
    except Exception as ex:
        print(ex)
        print('No video URL found')
        return('')
        

driver = driver_init()
driver.get(URL_0_0)
fb_sign_in(driver)
print('0 0 Course page opened')

meta = []
    
while(1):
    try:
        with open('links.txt','a+') as f:
            l = [el.text for el in driver.find_elements_by_xpath(PARENT_BREADCRUM)]
            l.append(driver.find_element_by_xpath(CURRENT_BREADCRUM).text)
            video_url = get_video_url(driver)
            if video_url:
                l.append(video_url)
                file_size = get_file_size(video_url)
                l.append(int(file_size)/1048576.0)
                f.write(str(l)+'\n')
                meta.append(l)
            try:
                nxt_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, NEXT_BUTTON)))
    #             nxt_btn = driver.find_element_by_xpath(NEXT_BUTTON)
                nxt_btn.click()
            except Exception as ex:
                print(ex)
                print(meta) 
                driver.close()
                exit()
    except Exception as ex:
            print(ex)
            print(meta)
            driver.close() 
            exit()
print(meta) 
driver.close()
