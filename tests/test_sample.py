import json
from typing import Sequence, cast

from pydantic import parse_obj_as
from requests.cookies import MockResponse
from twilio.rest import Client
from kabuto.main import get_twilio_client, notify, scan_for_tickets
from kabuto._types import TicketAvailabilityResponse, Ticket


SAMPLE_JSON_RESPONSE = '{"tickets":[{"id":94643,"event_id":26753,"available":0,"dynamic":0,"freesale":false,"sold_out":true,"status":"SOLD_OUT"},{"id":94644,"event_id":26753,"available":0,"dynamic":0,"freesale":false,"sold_out":true,"status":"SOLD_OUT"}]}'


def test_pydantic_deserialise():
    response = parse_obj_as(TicketAvailabilityResponse, json.loads(SAMPLE_JSON_RESPONSE))

    assert response.tickets[0].available == 0
    assert response.tickets[1].available == 0


class DummyTwilioMessageCreateResponse:
    def __init__(self, sid):
        self.sid = sid

class MockTwilioClient:
    @property
    def messages(self):
        return self

    def create(self, body, from_, to) -> DummyTwilioMessageCreateResponse:
        return DummyTwilioMessageCreateResponse("123")


def test_notify_tickets():
    tickets: Sequence[Ticket] = [
        Ticket(id=94643, event_id=26753, available=0, dynamic=0, freesale=False, sold_out=True, status="SOLD_OUT"),
        Ticket(id=94644, event_id=26753, available=0, dynamic=0, freesale=False, sold_out=True, status="SOLD_OUT"),
    ]
    client = cast(Client, MockTwilioClient())
    msgs = notify(client, tickets)

    assert len(msgs) == 2

class MockRequestsGetResponse:
    def __init__(self, _json):
        self._json = json.loads(_json)

    def json(self):
        return self._json


def test_scan_for_tickets(mocker):
    mocker.patch("requests.get", return_value=MockRequestsGetResponse(SAMPLE_JSON_RESPONSE))
    tickets = scan_for_tickets()

    assert len(tickets) == 0
