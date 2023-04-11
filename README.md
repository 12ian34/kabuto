# kabuto

Kaboodle ticket resale watcher

## Usage
### Pre-requisites
- You have [poetry](https://python-poetry.org/docs/#installation) installed
- You have run:

```bash
$ poetry install
```

### What you'll need
1. Twilio free trial account which you'll get from the dashboard:
- Twilio Account SID
- Twilio Auth Token
- Twilio Number
2. Your mobile number (with extension code i.e `+44` for UK)
3. Kaboodle event info
- Package ID (example - grab `18381` from `https://bookings.kaboodle.co.uk/book/18381/ticket`)
- Kaboodle Cookie, you can grab this by visiting the Kaboodle booking page of interest,
  go to the Developer Tools of your browser of choice, visit the network tab,
  reload the page & navigate to the request being made by your browser to `https://bookings.kaboodle.co.uk/api/4.0/package/ticketavailability`.
  Find the `Cookie` request header & copy the entire value (it might contain
  something like `kabFLOW`).
- [Optional] Ticket IDs - use the previous point but visit `Response` tab and
  expand the JSON to find the available ticket IDs for this package

### Using environment variables
```bash
$ cp .env.example .env
# fill in the .env file with your details
$ source .env
$ poetry run scan_for_tickets --package-id {PACKAGE_ID} --desire-all --interval 180
```

### Using CLI arguments
```bash
$ poetry run scan_for_tickets \
--package-id {PACKAGE_ID} --desire-all \
--twilio-sid {YOUR_SID} --twilio-token {YOUR_TOKEN} \
--twilio-number {YOUR_TWILIO_NUMBER} --my-number {MY_NUMBER} \
--kaboodle-cookie {COOKIE_STRING} \
--interval 180 \
```

### Alert for some tickets
```bash
$ source .env
$ poetry run scan_for_tickets \
--package-id {PACKAGE_ID} -w {TICKET_ID} -w {TICKET_ID} \
--interval 180 \
```

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
