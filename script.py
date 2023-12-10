import argparse
import os
import regex as re
import random
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from amazoncaptcha import AmazonCaptcha
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.CRITICAL)

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



def createDriver():
    print("Creating driver...")

    # Define the Chrome webdriver options
    options = Options()
    # Set the Chrome webdriver to run in headless mode for scalability
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.headless = True

    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.add_experimental_option('prefs', prefs)

    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")
    # help minimize crash
    options.add_argument("--disable-dev-shm-usage")
    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    # Turn-off userAutomationExtension
    options.add_experimental_option("useAutomationExtension", False)
    # no log console
    options.add_argument("--log-level=OFF")


    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    options.page_load_strategy = "none"

    # Pass the defined options objects to initialize the web driver
    service = Service(executable_path=r'chromedriver\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

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
        title = driver.find_element(By.XPATH, "//*[@id='title']").text

        if '\n' in price:
            price = price.replace("\n",".")

    except:
        price = None
        title = None

    item = {"asin": asin, "price": price, "title": title}
    return item

def getAsins(driver, url):
    print("Get all asins in page...")
    print(url)

    driver.implicitly_wait(10)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragents[random.randint(0,len(useragents)-1)]})
    driver.execute_script("return navigator.userAgent;")
    driver.get(url)

    time.sleep(20)

    if "validateCaptcha" in driver.current_url:
        print("Captcha is requiring")
        solveCaptcha()
        time.sleep(5)


    elems = driver.find_elements(By.XPATH, "//a[@href]")

    asins = set()
    for elem in elems:
        link = elem.get_attribute("href")
        candidates = re.findall(r"/dp/([A-Z0-9]{10})/", link)
        for c in candidates:
            asins.add(c)

        candidates = re.findall(r"%2Fdp%2F([A-Z0-9]{10})", link)
        for c in candidates:
            asins.add(c)

    print(asins)
    return asins

def saveFile(items, writer, sheetName):
    print("Saving result to sheet ", sheetName)
    
    df = pd.DataFrame(items)
    df.to_excel(writer, sheet_name=sheetName, index=False)


def getListRootAsins(input_file='Map Data.xlsx', sheetName='Sheet1', colName='Asin Advertised', partition=1, n=200):
    df = pd.ExcelFile(input_file).parse(sheetName) #you could add index_col=0 if there's an index
    res = df[colName].tolist()

    start = partition * n
    end = (partition + 1) * n

    if start > len(res):
        return []
    
    if end > len(res):
        return res[start:]
    
    return res[start:end]


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file name", default='Map Data.xlsx')
    parser.add_argument("-c", "--column", help="column name", default='Asin Advertised')
    parser.add_argument("-s", "--sheet", help="sheet name", default='Sheet1')
    parser.add_argument("-o", "--output", help="output path (not filename)", default="output/")
    parser.add_argument("-n", "--num", help="number of asins per process", default=200, type=int)
    parser.add_argument("-p", "--partition", help="partition of input file (0->n)", required=True, type=int)

    args = parser.parse_args()

    rootAsins = getListRootAsins(args.input, args.sheet, args.column, int(args.partition), int(args.num))
    if len(rootAsins) == 0:
        print("empty asins")
        exit

    path = args.output
    driver = createDriver()

    _, input_filename = os.path.split(args.input)
    filename = input_filename.split(".")[0]
    output_file = os.path.join(path, filename + "_" + str(args.partition) + ".xlsx")
    print("Output to ", output_file)

    writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')

    for rootAsin in rootAsins:
        url = "https://www.amazon.com/dp/" + rootAsin
        asins = getAsins(driver, url)
        asins.discard(rootAsin)

        items = []
        for asin in asins:
            time.sleep(random.randint(0, 200) / 100)
            items.append(getItem(driver, asin))

        saveFile(items, writer, rootAsin)

    writer.close()
    driver.quit()

    print("~~~~~~~~~~ DONE ~~~~~~~~~~~~", args.partition)
    print("--- %s seconds ---" % (time.time() - start_time))