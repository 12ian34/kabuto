from datetime import timedelta
from os import environ as env

ACCOUNT_SID = env.get("TWILIO_SID")
AUTH_TOKEN = env.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = env.get("TWILIO_NUMBER")
MY_NUMBER = env.get("MY_NUMBER")
KABOODLE_COOKIE = env.get("KABOODLE_COOKIE")

API_URL = "https://bookings.printworkslondon.co.uk/api/4.0/package/ticketavailability"
QUERY_INTERVAL = timedelta(minutes=1).total_seconds()

DESIRED_PACKAGE_ID = 18381 # package id = which event but different from event_id in the JSON response
DESIRE_ALL_TICKETS = True # flag for all tickets
DESIRED_TICKET_IDS = [94643, 94644] # ticket id = which ticket type, pre-2pm etc
