import base64
import json
import os
import urllib
from urllib import request, parse


TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")


def lambda_handler(event, context):
    target_number = event['To']
    twilio_number = event['From']
    response_target = event['Response']
    base_message = "Message from: {} - ".format(response_target)
    body = base_message + event['Body']

    if not ACCOUNT_SID or if not AUTH_TOKEN:
        return "Unable to access Twilio: Account SID and Auth Token required."
    elif not target_number:
        return "The function needs a 'To' number in the format +12023351493"
    elif not twilio_number:
        return "The function needs a 'From' number in the format +19732644156"
    elif not body:
        return "The function needs a 'Body' message to send."

    # insert Twilio Account SID into the REST API URL
    final_url = TWILIO_SMS_URL.format(ACCOUNT_SID)
    post_params = {"To": target_number, "From": twilio_number, "Body": body}

    # encode the parameters for Python's urllib
    req = request.Request(final_url)
    data = parse.urlencode(post_params).encode()

    # add authentication header to request based on Account SID + Auth Token
    authentication = "{}:{}".format(ACCOUNT_SID, AUTH_TOKEN)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))

    try:
        # perform HTTP POST request
        with request.urlopen(req, data) as f:
            #print("function fired")
            print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
    except Exception as e:
        # something went wrong!
        print(e)

    return "SMS sent successfully!"
