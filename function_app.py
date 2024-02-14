import azure.functions as func
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger2", auth_level=func.AuthLevel.FUNCTION)
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080"); # Added to handle size in headless mode
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
    driver.set_page_load_timeout(20)
    browser_version = driver.capabilities['browserVersion']
    chrome_driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]

    print(browser_version)
    print(chrome_driver_version)

    print("Chrome Browser Version:", browser_version[0:3])
    print("Chrome Driver Version:", chrome_driver_version[0:3])

    driver.get("https://www.python.org")

    print("Hello World!!!!!!!, " + driver.title)


    time.sleep(5)

    wait = WebDriverWait(driver, 10)
    driver.get('https://news.ycombinator.com/')
    element_list = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title > a"))
    )
    for element in element_list:
        try:
            title, url = element.text, element.get_attribute('href')
            print("Title:", title, "\nURL:", url, end="\n\n")
        except Exception as e:
            print(e)

    time.sleep(5)
    driver.quit()


    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
