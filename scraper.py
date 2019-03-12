import requests
from requests.exceptions import RequestException
from contextlib import closing
from selenium import webdriver
#from pyvirtualdisplay import Display
import time
import datetime
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:password1234@cluster0-bzguy.gcp.mongodb.net/test?retryWrites=true")
db = client.test
collection = db.menu_data

def main():
    #date = 'Monday, March 11, 2019'
    date = get_date_today()
    data = scrape('breakfast', date)
    test_id = collection.insert_one(data)
    data = scrape('lunch', date)
    test_id = collection.insert_one(data)
    data = scrape('dinner', date)
    test_id = collection.insert_one(data)
    
    meals_MTWRFSa = ['breakfast', 'lunch', 'dinner']
    meals_Sun = ['breakfast', 'brunch', 'dinner']

    for i in range(0, 7):
        #if Sunday, get Sunday menu (brunch)
        if get_weekday_today() == 0:

        else:
            date = get_date_today()

def get_weekday_today():
    return datetime.datetime.today().weekday()

def get_date_today():
    day = datetime.datetime.today().day
    year = datetime.datetime.today().year
    weekday = ''
    month = ''

    if(datetime.datetime.today().month == 1):
        month = 'January'
    elif(datetime.datetime.today().month == 2):
        month = 'February'
    elif(datetime.datetime.today().month == 3):
        month = 'March'
    elif(datetime.datetime.today().month == 4):
        month = 'April'
    elif(datetime.datetime.today().month == 5):
        month = 'May'
    elif(datetime.datetime.today().month == 6):
        month = 'June'
    elif(datetime.datetime.today().month == 7):
        month = 'July'
    elif(datetime.datetime.today().month == 8):
        month = 'August'
    elif(datetime.datetime.today().month == 9):
        month = 'September'
    elif(datetime.datetime.today().month == 10):
        month = 'October'
    elif(datetime.datetime.today().month == 11):
        month = 'November'
    elif(datetime.datetime.today().month == 12):
        month = 'December'
    else:
        month = ''

    if(datetime.datetime.today().weekday() == 0):
        weekday = 'Monday'
    elif(datetime.datetime.today().weekday() == 1):
        weekday = 'Tuesday'
    elif(datetime.datetime.today().weekday() == 2):
        weekday = 'Wednesday'
    elif(datetime.datetime.today().weekday() == 3):
        weekday = 'Thursday'
    elif(datetime.datetime.today().weekday() == 4):
        weekday = 'Friday'
    elif(datetime.datetime.today().weekday() == 5):
        weekday = 'Saturday'
    elif(datetime.datetime.today().weekday() == 6):
        weekday = 'Sunday'
    else:
        weekday = ''
    date_str = weekday + ', ' + month + ' ' + str(day) + ', ' + str(year)
    return date_str

def scrape(meal, date):
    quote_page = 'http://sjumenu.csbsju.edu/NetNutrition/1'
    browser = webdriver.Chrome()
    browser.get(quote_page)
    elem = browser.find_element_by_class_name('cbo_nn_menuTable')
    children = elem.find_elements_by_class_name('cbo_nn_menuCell')
    resp_dict = {}
    done = False
    resp_dict['date'] = date
    resp_dict['meal'] = meal
    for child in children:
        if done:
            break
        if date in child.text:
            meal_links = child.find_elements_by_class_name('cbo_nn_menuLink')
            for link in meal_links:
                if meal.upper() in link.text:
                    link.click()
                    time.sleep(3)
                    menu_items = browser.find_elements_by_class_name('cbo_nn_itemHover')
                    count = 0
                    for menu_item in menu_items:
                        resp_dict[str(count)] = menu_item.text
                        count+=1
                    done = True
                    break
    browser.close()
    return resp_dict

if __name__ == "__main__":
    main()