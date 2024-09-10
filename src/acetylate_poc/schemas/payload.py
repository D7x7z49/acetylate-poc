from __future__ import annotations
from typing import Optional, Annotated
from dataclasses import dataclass

@dataclass
class HttpPayload:
    data: str
    headers: Optional[dict[str, str]] = None

@dataclass
class TcpPayload:
    data: str

@dataclass
class Payload:
    type: Annotated[str, "The type of payload, which determines the format and content of the payload data."]
    http: Optional[HttpPayload] = None
    tcp: Optional[TcpPayload] = None

    def __post_init__(self):
        if self.type == 'http' and self.http is None:
            raise ValueError("When type is 'http', 'http' field must be provided.")
        if self.type == 'tcp' and self.tcp is None:
            raise ValueError("When type is 'tcp', 'tcp' field must be provided.")
        if self.type not in ['http', 'tcp']:
            raise ValueError("Invalid payload type.")
