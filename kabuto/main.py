import functools
import time
import click
import backoff
from datetime import datetime
from typing import Mapping, Optional, Sequence

import requests
from pydantic import parse_obj_as
from twilio.http import TwilioException
from twilio.rest import Client

from kabuto._types import Ticket, TicketAvailabilityResponse
from kabuto.click import validate
from kabuto.config import (ACCOUNT_SID, API_URL, AUTH_TOKEN,
                           DESIRE_ALL_TICKETS, DESIRED_PACKAGE_ID,
                           DESIRED_TICKET_IDS, KABOODLE_COOKIE, MY_NUMBER,
                           QUERY_INTERVAL, TWILIO_NUMBER)


def get_twilio_client(account_sid: str, token: str) -> Client:
    return Client(account_sid, token)

def get_requests_client() -> requests.Session:
    return requests.Session()

def build_headers(package_id: int, kaboodle_cookie: str) -> Mapping[str, str]:
    _package_id = str(package_id)
    return {
        "package-id": _package_id,
        "referer": f"https://bookings.printworkslondon.co.uk/book/{_package_id}/ticket",
        "accept": "application/json",
        "cookie": kaboodle_cookie,
    }


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def get_response(
    client: requests.Session, desired_package_id: int, kaboodle_cookie: str
) -> TicketAvailabilityResponse:
    headers = build_headers(desired_package_id, kaboodle_cookie)
    response = client.get(API_URL, allow_redirects=True, headers=headers)
    print(f"Reached Kaboodle at {str(datetime.now())}", flush=True)
    if response.status_code != 200:
        raise RuntimeError(f"Kaboodle responded with {response.json()}")

    return parse_obj_as(TicketAvailabilityResponse, response.json())


def desirable(desire_all_flag: bool, desired_list: Sequence[int], item: Ticket) -> bool:
    return item.purchasable and (desire_all_flag or item.id in desired_list)


def scan_for_tickets(
    client: requests.Session,
    desired_package_id: int,
    desired_ticket_ids: Sequence[int],
    desire_all_tickets: bool,
    kaboodle_cookie: str,
) -> Sequence[Ticket]:
    response = get_response(client, desired_package_id, kaboodle_cookie)
    desirable_ticket = functools.partial(
        desirable, desire_all_tickets, desired_ticket_ids
    )
    return list(filter(desirable_ticket, response.tickets))


@backoff.on_exception(backoff.expo, TwilioException, max_tries=5)
def notify(
    twilio_client: Client,
    tickets: Sequence[Ticket],
    desired_package_id: int,
    my_number: str,
    twilio_number: str,
) -> Sequence[Optional[str]]:
    return [
        twilio_client.messages.create(
            body=f"ticket available! https://queue.kaboodle.co.uk/?c=kaboodle&e=kaboodlequeue&t_client_id=39&t_agent_id=408740&t_package_id={desired_package_id}",
            from_=twilio_number,
            to=my_number,
        ).sid
        for _ in tickets
    ]


@click.command()
@click.option("--package-id", default=DESIRED_PACKAGE_ID, help="Event ID from Kaboodle URL")
@click.option("--twilio-sid", default=ACCOUNT_SID, help="Twilio Account SID from dashboard")
@click.option("--twilio-token", default=AUTH_TOKEN, help="Twilio Auth Token from dashboard")
@click.option("--twilio-number", default=TWILIO_NUMBER, help="Twilio phone number from dashboard")
@click.option("--my-number", default=MY_NUMBER, help="Your phone number to notify")
@click.option("--kaboodle-cookie", default=KABOODLE_COOKIE, help="Kaboodle cookie from browser dev tools, see README for more info")
@click.option("--desire-all/--no-desire-all", default=DESIRE_ALL_TICKETS, help="Flag to scan for all tickets")
@click.option("--wanted-ticket-id", '-w', multiple=True, required=False, default=DESIRED_TICKET_IDS, help="Wanted Ticket IDs")
@click.option("--interval", default=QUERY_INTERVAL, help="Query interval in seconds")
def scan(
    package_id,
    twilio_sid,
    twilio_token,
    twilio_number,
    my_number,
    kaboodle_cookie,
    desire_all,
    wanted_ticket_id,
    interval,
):
    validate([
        (twilio_sid, f"{twilio_sid=}"),
        (twilio_token, f"{twilio_token=}"),
        (twilio_number, f"{twilio_number=}"),
        (my_number, f"{my_number=}"),
        (kaboodle_cookie, f"{kaboodle_cookie=}"),
    ])
    twilio_client = get_twilio_client(twilio_sid, twilio_token)
    kaboodle_client = get_requests_client()
    while True:
        available_tickets = scan_for_tickets(kaboodle_client, package_id, wanted_ticket_id, desire_all, kaboodle_cookie)
        messages = notify(twilio_client, available_tickets, package_id, my_number, twilio_number)
        print(f"Sent {len(messages)} messages with SIDs {messages=} at {str(datetime.now())}", flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    scan() # type: ignore
