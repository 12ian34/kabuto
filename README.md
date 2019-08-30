# kabuto

## Context

**Kaboodle** is a service that sells tickets to events, mainly electronic music at Printworks in London. For some events where the tickets have sold out, a "Resale queue" is made active. If one would like to attend a sold out event with the resale queue active, they would need to keep entering the Resale queue link and hoping some tickets were made available since there is no notification option. 

**Twilio** is an API platform company which provides a tool to programmatically send text messages. One can sign up for a free trial which provides £15 free credit.

## Functionality

`kabuto` is a python script that checks the resale queue - at an imperfectly defined interval - for available tickets to a particular event and sends a text message when at least 1 ticket becomes available.

## Limitations

- one must manually find the event ID for the event of interest, and amend the script accordingly.
- one must manually create a Twilio account, and also have a mobile number. The relevant details must then be set as Environment Variables for the script to pick up.
- one must manually obtain the Stripe cookie after selecting the resale link and assign it to the relevant Environment Variable.
- the defined interval doesn't take into account the time it takes to run the script. This isn't very Pythonic but I don't care.
- text messages will keep being sent for as long as tickets are available, potentially wasting Twilio credit.

## Future work

- get the right cookie and assign it to the relevant Environment Variable, automatically.
- implement interactive function for setting Environment Variables according to the relevant Twilio and phone number details. 
- implement interactive function for choosing and setting the correct event ID. 
