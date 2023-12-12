import argparse
import os
import regex as re
import random
import time 
from datetime import date
import pandas as pd 
from PIL import Image
import urllib
import urllib.request
from openpyxl.drawing.image import Image as OImage

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


def getItem(driver, asin, showImg=False):
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

        if showImg:
            img = driver.find_element(By.XPATH, '//*[@id="landingImage"]').get_attribute("src")

    except Exception as e:
        price = None
        title = None
        img = None
        print("LOI", e)


    item = {"asin": asin, "price": price, "title": title}
    if showImg:
        item["img"] = img
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
        candidates = re.findall(r"/dp/([A-Z0-9]{10})/", link)
        for c in candidates:
            asins.add(c)

        candidates = re.findall(r"%2Fdp%2F([A-Z0-9]{10})", link)
        for c in candidates:
            asins.add(c)

    print(asins)
    return asins


def saveFile(items, writer, sheetName):
    print("Saving result to sheet")
    url = items[0].pop('img', None)
    img_name = getImg(url)

    df = pd.DataFrame(items)
    df.to_excel(writer, sheet_name=sheetName, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    worksheet = writer.sheets[sheetName]
    worksheet.add_image(OImage(img_name), "F0")

    os.remove(img_name)

def getImg(url):
    img_name = os.path.join("tmp", str(time.time()) + '.jpg')
    urllib.request.urlretrieve(url, img_name) # Save image

    # Convert image
    img = Image.open(img_name)
    img.thumbnail((128, 128))
    img.save(img_name)

    return img_name

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

    path = createFolder(args.output)
    driver = createDriver()

    sheet_name = str(date.today())

    for rootAsin in rootAsins:
        url = "https://www.amazon.com/dp/" + rootAsin
        asins = getAsins(driver, url)
        asins.discard(rootAsin)

        items = []
        items.append(getItem(driver, rootAsin, True))
        for asin in asins:
            time.sleep(random.randint(0, 200) / 100)
            items.append(getItem(driver, asin))

        output_filename = path + rootAsin + ".xlsx"
        
        if not os.path.exists(output_filename):
            writer = pd.ExcelWriter(output_filename, engine="openpyxl")
        else:
            writer = pd.ExcelWriter(output_filename, engine="openpyxl",mode='a',if_sheet_exists="replace")
            
        saveFile(items, writer, sheet_name)
        writer.close()

    driver.quit()



   
