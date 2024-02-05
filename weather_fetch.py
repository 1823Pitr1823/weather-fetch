#!venv/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import os
from notifypy import Notify
engine=""

#Prepares web scraper and outputs it into global variable "engine"
def run_scraper():
    global engine
    foptions = webdriver.FirefoxOptions()
    foptions.add_argument('--headless')
    foptions.add_argument("--window-size=1920,1080")
    foptions.add_argument('--start-maximized')
    foptions.add_argument('--disable-gpu')
    foptions.add_argument('--no-sandbox')
    foptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    engine=webdriver.Firefox(options=foptions)
    
#Handles searches in google search engine input searched prompt
def search_google(text):
    engine.get("https://www.google.com/")
    assert "Google"
    engine.find_element(By.ID, "W0wltc").click()
    elem = engine.find_element(By.TAG_NAME, "textarea")
    elem.click()
    elem.send_keys(text+ Keys.RETURN)

#Gets current weather and sends it to system notifications
def get_weather():
    run_scraper()
    search_google("current weather")
    engine.implicitly_wait(3)
    elem2=engine.find_element(By.ID, "wob_tci")
    url_i=elem2.get_attribute("src")
    url_t=elem2.get_attribute("alt")
    url_temp=engine.find_element(By.ID, "wob_tm").text
    print(url_temp)
    subprocess.call(["curl","-o",os.getcwd()+"/c_weather.png",url_i])
    
    notification = Notify()
    notification.title = "Weather"
    notification.message = url_t+" "+url_temp+"˚C"
    notification.icon="c_weather.png"
    notification.send()
    engine.quit()

if __name__=="__main__":
    get_weather()


