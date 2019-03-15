import requests
from requests.exceptions import RequestException
from contextlib import closing
from selenium import webdriver
import time
import datetime
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:password1234@cluster0-bzguy.gcp.mongodb.net/test?retryWrites=true")
db = client.test
collection = db.menu_data

def main():
    #date = 'Monday, March 11, 2019'
    collection.remove()
    data = scrape()
    for item in data:
        test_id = collection.insert_one(item)

def get_weekday_today():
    return datetime.datetime.today().weekday()

def scrape():
    quote_page = 'http://sjumenu.csbsju.edu/NetNutrition/1'
    browser = webdriver.Chrome()
    browser.get(quote_page)
    elem = browser.find_element_by_class_name('cbo_nn_menuTable')
    children = elem.find_elements_by_class_name('cbo_nn_menuCell')

    dates_list = {}
    dates_list['dates_list'] = 'test'
    dt_ct = 0
    dates = []
    for child in children:
        info = child.text
        split_info = info.split('\n')
        dates_list[str(dt_ct)] = split_info[0]
        dates.append(split_info[0])
        dt_ct += 1
    test_id = collection.insert_one(dates_list)
    weekend_meals = ['breakfast', 'brunch', 'dinner']
    weekday_meals = ['breakfast', 'lunch', 'dinner']

    menu_days = []

    for date in dates:
        if "Sunday" in date or "Saturday" in date:
            for meal in weekend_meals:
                resp_dict = {}
                done = False
                resp_dict['date'] = date
                resp_dict['meal'] = meal
                time.sleep(0.25)
                elem = browser.find_element_by_class_name('cbo_nn_menuTable')
                children = elem.find_elements_by_class_name('cbo_nn_menuCell')
                for child in children:
                    if done:
                        break
                    if date in child.text:
                        meal_links = child.find_elements_by_class_name('cbo_nn_menuLink')
                        for link in meal_links:
                            if meal.upper() in link.text:
                                link.click()
                                time.sleep(0.25)
                                menu_items = browser.find_elements_by_class_name('cbo_nn_itemHover')
                                count = 0
                                for menu_item in menu_items:
                                    resp_dict[str(count)] = menu_item.text
                                    count+=1
                                done = True
                                menu_days.append(resp_dict)
                                back = browser.find_element_by_id('btn_Back1')
                                back.click()
                                time.sleep(1)
                                break
        else:
            for meal in weekday_meals:
                resp_dict = {}
                done = False
                resp_dict['date'] = date
                resp_dict['meal'] = meal
                time.sleep(0.25)
                elem = browser.find_element_by_class_name('cbo_nn_menuTable')
                children = elem.find_elements_by_class_name('cbo_nn_menuCell')
                for child in children:
                    if done:
                        break
                    if date in child.text:
                        meal_links = child.find_elements_by_class_name('cbo_nn_menuLink')
                        for link in meal_links:
                            if meal.upper() in link.text:
                                link.click()
                                time.sleep(0.25)
                                menu_items = browser.find_elements_by_class_name('cbo_nn_itemHover')
                                count = 0
                                for menu_item in menu_items:
                                    resp_dict[str(count)] = menu_item.text
                                    count+=1
                                done = True
                                menu_days.append(resp_dict)
                                back = browser.find_element_by_id('btn_Back1')
                                back.click()
                                time.sleep(1)
                                break

    browser.close()
    return menu_days

if __name__ == "__main__":
    main()