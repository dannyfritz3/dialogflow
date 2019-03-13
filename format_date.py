import pymongo
import datetime

def format_date(date):
    split_text = date.split('T')
    split_date = split_text[0].split('-')
    year = split_date[0]
    month = split_date[1]
    day = split_date[2]
    weekday = datetime.date(int(year), int(month), int(day)).weekday()
    if(month == '01'):
        month = 'January'
    elif(month == '02'):
        month = 'February'
    elif(month == '03'):
        month = 'March'
    elif(month == '04'):
        month = 'April'
    elif(month == '05'):
        month = 'May'
    elif(month == '06'):
        month = 'June'
    elif(month == '07'):
        month = 'July'
    elif(month == '08'):
        month = 'August'
    elif(month == '09'):
        month = 'September'
    elif(month == '10'):
        month = 'October'
    elif(month == '11'):
        month = 'November'
    elif(month == '12'):
        month = 'December'
    else:
        month = ''
    
    if(weekday == 0):
            weekday = 'Monday'
    elif(weekday == 1):
        weekday = 'Tuesday'
    elif(weekday == 2):
        weekday = 'Wednesday'
    elif(weekday == 3):
        weekday = 'Thursday'
    elif(weekday == 4):
        weekday = 'Friday'
    elif(weekday == 5):
        weekday = 'Saturday'
    elif(weekday == 6):
        weekday = 'Sunday'
    else:
        weekday = ''
    date_str = weekday + ', ' + month + ' ' + str(day) + ', ' + str(year)
    return date_str

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

def main():
    test_date = '2019-03-12T12:00:00-05:00'
    formatted_date = format_date(test_date)
    print(formatted_date)
    client = pymongo.MongoClient("mongodb+srv://admin:password1234@cluster0-bzguy.gcp.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db['menu_data']

    data = collection.find_one({"$and":[{"meal":"dinner"},{"date":formatted_date}]})
    print(data)
    print(get_date_today())

if __name__ == '__main__':
    main()