from typing import Sequence, TypedDict
from pydantic import BaseModel

class Ticket(BaseModel):
    id: int
    event_id: int
    available: int
    dynamic: int
    freesale: bool
    sold_out: bool
    status: str

    @property
    def purchasable(self) -> bool:
        return self.available > 0

class TicketAvailabilityResponse(BaseModel):
    tickets: Sequence[Ticket]
