# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging

from flask import Flask, request, make_response, jsonify
import pymongo
from format_date import format_date, get_date_today
import datetime

try:
    import googleclouddebugger
    googleclouddebugger.enable()
except ImportError:
    pass

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://admin:password1234@cluster0-bzguy.gcp.mongodb.net/test?retryWrites=true")
db = client.test
collection = db['menu_data']
# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    # fetch meal and date from json
    meal = req.get('queryResult').get('parameters').get('meal')
    date = req.get('queryResult').get('parameters').get('date')
    formatted_date = ''
    if date == '':
        formatted_date = get_date_today()
    else:
        formatted_date = format_date(date)
    #get menu data from database
    data = collection.find_one({"$and":[{"meal":meal},{"date":formatted_date}]})
    resp_str = build_response(data, meal)
    return {'fulfillmentText':resp_str}

def build_response(data, meal):
    meta_data = ['_id', 'date', 'meal']
    if len(data) > 0:
        build_str = ''
        count = 0
        for i in data:
            if i not in meta_data:
                if count == len(data - 1):
                    build_str += "and " + data.get(i) + "."
                else:
                    build_str += data.get(i) + ", "
            count += 1
        full_str = 'Today for ' + meal + ', the reef will be serving ' + build_str
        return full_str
    else:
        return 'Sorry, couldn\'t find any information on that.'

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