from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import time

FORM_URL = "YOUR GOOGLE FORM"
ZILLOW_URL = "YOUR ZILLOW LISTING PAGE URL"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/16.1 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(ZILLOW_URL, headers=headers).text
soup = BeautifulSoup(response, "html.parser")
json_dict = soup.find_all("script", attrs={"type": "application/json"})
rentals = json_dict[1].text
rentals = rentals.replace("<!--", "")
rentals = rentals.replace("-->", "")
rentals = json.loads(rentals)
# print(rentals)

link_list = []
for i in rentals["cat1"]["searchResults"]["listResults"]:
    link = i["detailUrl"]
    link_list.append(link)

price_list = []
for i in rentals["cat1"]["searchResults"]["listResults"]:
    try:
        price = i["price"]
        price_list.append(price)

    except KeyError:
        price = i["units"][0]["price"]
        price_list.append(price)

new_price_list = []
for new in price_list:
    # print(type(new))
    new_price_list.append(new[:6])

price_list = new_price_list

address_list = []
for i in rentals["cat1"]["searchResults"]["listResults"]:
    address = i["address"]
    address_list.append(address)

driver = webdriver.Safari()
for i in range(len(link_list)):
    driver.get(FORM_URL)
    time.sleep(1)

    address_entry = driver.find_element(by=By.XPATH, value="XPATH FOR YOUR FORM ADDRESS INPUT")
    address_entry.send_keys(address_list[i])

    price_entry = driver.find_element(by=By.XPATH, value="XPATH FOR YOUR FORM PRICE INPUT")
    price_entry.send_keys(price_list[i])

    link_entry = driver.find_element(by=By.XPATH, value="XPATH FOR YOUR FORM LISTING URL INPUT")
    link_entry.send_keys(link_list[i])
    submit = driver.find_element(by=By.XPATH, value='XPATH FOR SUBMIT BUTTON')
    submit.click()
