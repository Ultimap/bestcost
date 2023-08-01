import time
import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

search = input()
urls = {
    'https://www.citilink.ru/search/?text=': ['sitilink', 'app-catalog-9gnskf e1259i3g0',
                                              'e1j9birj0 e106ikdt0 app-catalog-175fskm e1gjr6xo0'],
    'https://www.mvideo.ru/product-list-page?q=': ['mvideo', 'product-title__text product-title--clamp',
                                                   'price__main-value'],
}

yandex = {
    'url': 'https://market.yandex.ru',
    'market': 'yandex',
    'captcha': '//*[@class ="CheckboxCaptcha-Button"]',
    'find': '//*[@class = "_2onsR mini-suggest__input"]',
    'submit': '//button[@class = "V9Xu6 _3RXxZ _1LG7Q _3iB1w mini-suggest__button"]',
    'title': '//*[@class = "f0MCF _2tgvL cia-cs"]',
    'link': '//a[@class ="egKyN _2Fl2z"]',
    'item_cost': '//span[@data-auto= "price-value"]'
}

result = []


def parse(search_item):
    for x in urls.keys():
        driver = webdriver.Edge()
        search_item = search_item.replace(' ', '+')
        url = f'{x}{search_item}'
        driver.get(url)
        time.sleep(2)
        try:
            market = urls[x][0]
            item = driver.find_element(By.XPATH, f'//*[@class = "{urls[x][1]}"]')
            item_data = {
                'market': market,
                'title': item.text,
                'item_cost': int(driver.find_element(By.XPATH,
                                                     f'//*[@class = "{urls[x][2]}"] ').text.
                                 replace(' ₽', '').replace(" ", '')),
                'link': item.get_attribute('href')
            }
            result.append(item_data)
        except:
            pass
        finally:
            driver.quit()


def parse_yandex_market(search_item):
    driver = webdriver.Edge()
    driver.get(yandex['url'])
    enter_captcha_ya(driver)
    time.sleep(5)
    try:
        finder = driver.find_element(By.XPATH, yandex['find'])
        finder.send_keys(search_item)
        button = driver.find_element(By.XPATH, yandex['submit'])
        button.click()
        enter_captcha_ya(driver)
        item_data = {
            'market': yandex['market'],
            'title': driver.find_element(By.XPATH, yandex['title']).text,
            'item_cost': int(
                driver.find_element(By.XPATH, yandex['item_cost']).text.replace('\u2009', '').replace('\n₽', '')),
            'link': driver.find_element(By.XPATH, yandex['link']).get_attribute('href')
        }
        result.append(item_data)
    except:
        pass
    finally:
        driver.quit()


def enter_captcha_ya(driver):
    try:
        captcha = driver.find_element(By.XPATH, yandex['captcha'])
        captcha.submit()
    except:
        pass


def all_market_parse(search_item):
    parse(search_item)
    parse_yandex_market(search_item)
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    print("JSON-данные успешно записаны в файл output.json")


all_market_parse(search)
