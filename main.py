import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

URL = "https://flight.naver.com/"


def compute_date(dates, target) -> list:
    print("compute entire date information from current month to limit")
    return [date for date in dates if date.text == str(target)]


browser = webdriver.Chrome()
# browser.maximize_window()

browser.get(URL)
time.sleep(1)

# remove AD popup
find = browser.find_elements(By.CLASS_NAME, "anchor")
for f in find:
    if f.get_attribute("title") == "지금 바로 혜택 확인하기":
        browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
        print("remove pop up")
        break
time.sleep(1)

from_place = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[1]/b'
to_place = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]/b'
korea = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/section/button[1]'
gmp = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/section/div/button[4]/span/i[1]'
jeju = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/section/div/button[2]/span/i[1]'
search = '//*[@id="__next"]/div/div[1]/div[4]/div/div/button/span'
select = '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div/button'

# select from GMP
browser.find_element(By.XPATH, from_place).click()
print("select from air port")
time.sleep(1)
browser.find_element(By.XPATH, korea).click()
print("select korea(local)")
time.sleep(1)
browser.find_element(By.XPATH, gmp).click()
print("select GMP")
time.sleep(1)

# select to JEJU
browser.find_element(By.XPATH, to_place).click()
print("select to air port")
time.sleep(1)
browser.find_element(By.XPATH, korea).click()
print("select korea(local)")
time.sleep(1)
browser.find_element(By.XPATH, jeju).click()
print("select JEJU")
time.sleep(1)

# push 가는 날 button also delay 1 sec is necessary, if don't use this, can not read date information.
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]').click()
print("press start the travel date")
time.sleep(1)

# read date information and push 20 day
dates = browser.find_elements(By.CLASS_NAME, "sc-evZas dDVwEk num".replace(" ", "."))
compute_date(dates, 20)[0].click()
print("press 20")

# read date information and push 24 day
dates = browser.find_elements(By.CLASS_NAME, "sc-evZas dDVwEk num".replace(" ", "."))
compute_date(dates, 24)[0].click()
print("press 24")

# press search button
browser.find_element(By.XPATH, search).click()
print("press search button")

print("wait till display update")
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, select)))
print("done")

browser.find_element(By.XPATH, select).click()
time.sleep(1)
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div/div/button[1]/span').click()
print("press 가격 낮은순")
time.sleep(1)

res = BeautifulSoup(browser.page_source, "lxml")
flights = res.find_all("div", attrs={"class": "domestic_Flight__sK0eA result"})

flight_info = {"start": {}, "end": {}}
# for flight in flights:
#     print(flight.text)
#     print(flight.find("b", attrs={"class": "name"}).text)
#     print(flight.find_all("b", attrs={"class": "route_time__-2Z1T"})[0].text)
#     print(flight.find_all("b", attrs={"class": "route_time__-2Z1T"})[1].text)
#     print(flight.find("i", attrs={"class": "domestic_num__2roTW"}).text)

flight_info.update({
    "start": {
        "line": flights[0].find("b", attrs={"class": "name"}).text,
        "start": flights[0].find_all("b", attrs={"class": "route_time__-2Z1T"})[0].text,
        "end": flights[0].find_all("b", attrs={"class": "route_time__-2Z1T"})[1].text,
        "price": flights[0].find("i", attrs={"class": "domestic_num__2roTW"}).text
    }
})

print("select one")
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[2]/div[2]/div/button').click()
time.sleep(1)

print("press 출발시간 빠른 순")
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[2]/div/div/button').click()
time.sleep(1)

print("press 가격 낮은 순")
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[2]/div/div/div/button[1]/span').click()
time.sleep(1)

res = BeautifulSoup(browser.page_source, "lxml")
flights = res.find_all("div", attrs={"class": "domestic_Flight__sK0eA result"})

flight_info.update({
    "end": {
        "line": flights[0].find("b", attrs={"class": "name"}).text,
        "start": flights[0].find_all("b", attrs={"class": "route_time__-2Z1T"})[0].text,
        "end": flights[0].find_all("b", attrs={"class": "route_time__-2Z1T"})[1].text,
        "price": flights[0].find("i", attrs={"class": "domestic_num__2roTW"}).text
    }
})

print("select one")
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[3]/div[2]/div/button').click()

total_price = int(flight_info["start"]["price"].replace(",", "")) + int(flight_info["end"]["price"].replace(",", ""))
total_price = format(total_price, ",")
information = f"""
가는편
항공사 : {flight_info["start"]["line"]}
출발 시간 : {flight_info["start"]["start"]}
도착 시간 : {flight_info["start"]["end"]}
편도 가격 : {flight_info["start"]["price"]}

오는편
항공사 : {flight_info["end"]["line"]}
출발 시간 : {flight_info["end"]["start"]}
도착 시간 : {flight_info["end"]["end"]}
편도 가격 : {flight_info["end"]["price"]}

전체 항공권 가격 : {total_price}
"""
print(information)
while True:
    pass
