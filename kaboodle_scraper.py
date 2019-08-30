import requests
import time
import os
from twilio.rest import Client
from datetime import datetime

account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_NUMBER"]
my_number = os.environ["MY_NUMBER"]

api_url = "https://bookings.kaboodle.co.uk/api/package/ticketavailability"
api_headers = {'package-id': '9261',
           'referer':'https://bookings.kaboodle.co.uk/book/9261/ticket',
           'accept': 'application/json',
           'cookie': os.environ["KABOODLE_COOKIE"]
          }

def count_tickets():
    
    apiurl = api_url
    headers = api_headers
    response = requests.get(apiurl, allow_redirects=True, headers=headers)
    print("\n" + str(datetime.now()) + "\n")
    print(str(response.json()) + "\n")

    for item in response.json()['tickets']:
        
        if item['@id'] == 5324:
            
            tickets_available = item['@available']
            
            print("There are " + str(tickets_available) + " tickets available")
            
            if tickets_available > 0:

                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body = "ticket available! https://queue.kaboodle.co.uk/?c=kaboodle&e=kaboodlequeue&t_client_id=39&t_agent_id=408740&t_package_id=9261",
                    from_= twilio_number,
                    to = my_number
                )

                print(message.sid)


starttime=time.time()

while True:
  count_tickets()
  time.sleep(100)
