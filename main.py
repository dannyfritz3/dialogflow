import logging

from flask import Flask, request, make_response, jsonify
import pymongo
from utility import format_date, get_date_today, build_response
import datetime

#enables debugging in google cloud console
try:
    import googleclouddebugger
    googleclouddebugger.enable()
except ImportError:
    pass

app = Flask(__name__)
#establishing a client connection with database (mongodb)
client = pymongo.MongoClient("mongodb+srv://admin:password1234@cluster0-bzguy.gcp.mongodb.net/test?retryWrites=true")
db = client.test
#retrieve the menu-data collection
collection = db['menu_data']
# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    # fetch meal and date from json packet
    meal = req.get('queryResult').get('parameters').get('meal')
    date = req.get('queryResult').get('parameters').get('date')
    formatted_date = ''
    #if no date specified from user, use today's date
    if date == '':
        formatted_date = get_date_today()
    else:
        formatted_date = format_date(date)
    #get menu data from database
    data = collection.find_one({"$and":[{"meal":meal},{"date":formatted_date}]})
    resp_str = build_response(data, meal, formatted_date)
    return {'fulfillmentText':resp_str}

# create a route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]