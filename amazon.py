import argparse
import os
import regex as re
import random
import time 
import pandas as pd 

from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from amazoncaptcha import AmazonCaptcha

amazon_captcha_url = "https://www.amazon.com/errors/validateCaptcha"

useragents=[
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    ]

def createFolder(path = r"amazon/"):
    print("Creating folder...")

    if not os.path.exists(path):
        os.makedirs(path)

    return path

def createDriver(headless=True):
    print("Creating driver...")

    # Define the Chrome webdriver options
    options = webdriver.ChromeOptions() 
    # Set the Chrome webdriver to run in headless mode for scalability
    if headless:
        options.add_argument("--headless") 
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 

    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    options.page_load_strategy = "none"

    # Pass the defined options objects to initialize the web driver 
    driver = Chrome(options=options) 

    return driver

def solveCaptcha():
    print("Solving captcha...")
    img_link = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute('src')
    captcha = AmazonCaptcha.fromlink(img_link)
    captcha_value = AmazonCaptcha.solve(captcha)

    input_field = driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
    button = driver.find_element(By.CLASS_NAME, "a-button-text")
    button.click()


def getItem(driver, asin):
    print("Get item price", asin)

    url = "https://www.amazon.com/dp/" + asin

    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragents[random.randint(0,len(useragents)-1)]}) 
    driver.execute_script("return navigator.userAgent;")
    driver.get(url) 

    if "validateCaptcha" in driver.current_url:
        print("Captcha is requiring")
        solveCaptcha()
        time.sleep(5)


    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price"))
        )

        price = element.text
        
        if '\n' in price:
            price = price.replace("\n",".")

    except:
        price = None

    item = {"asin": asin, "price": price}
    return item


def getAsins(driver, url):
    print("Get all asin in page...")
    print(url)

    driver.implicitly_wait(10)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragents[random.randint(0,len(useragents)-1)]}) 
    driver.execute_script("return navigator.userAgent;")
    driver.get(url)

    if "validateCaptcha" in driver.current_url:
        print("Captcha is requiring")
        solveCaptcha()
        time.sleep(5)
    
    time.sleep(20)

    elems = driver.find_elements(By.XPATH, "//a[@href]")

    asins = set()
    for elem in elems:
        link = elem.get_attribute("href")
        candidates = re.findall(r"/dp/(B0\w*)/", link)
        for c in candidates:
            asins.add(c)

    print(asins)
    return asins


def saveFile(items, file_name):
    print("Saving result to file ", file_name)

    df = pd.DataFrame(items)
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ra", "--rootasin", help="Asin of the product", required=True)
    parser.add_argument("-b", "--browser", help="Open Chrome browser to view process", action='store_const', const=True, default=False)
    parser.add_argument("-p", "--path", help="CSV ouput file folder", default="output/")

    args = parser.parse_args()

    rootAsin = args.rootasin

    url = "https://www.amazon.com/dp/" + rootAsin

    path = createFolder(args.path)
    driver = createDriver(not args.browser)
    
    asins = getAsins(driver, url)
    asins.discard(rootAsin)

    items = []
    for asin in asins:
        time.sleep(random.randint(0, 200) / 100)
        items.append(getItem(driver, asin))
    driver.quit()

    saveFile(items, path + rootAsin + ".csv")



   
