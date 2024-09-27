from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class TcpPayload(BaseModel):
    payload_type: Annotated[
        Literal["tcp"],
        Field(
            ...,
            title="Payload Type",
            description=("The type of payload, which determines the format and content of the payload data."),
        ),
    ]


class UdpPayload(BaseModel):
    payload_type: Annotated[
        Literal["udp"],
        Field(
            ...,
            title="Payload Type",
            description=("The type of payload, which determines the format and content of the payload data."),
        ),
    ]


class HttpPayload(BaseModel):
    payload_type: Annotated[
        Literal["http"],
        Field(
            ...,
            title="Payload Type",
            description=("The type of payload, which determines the format and content of the payload data."),
        ),
    ]
    method: Annotated[
        str,
        Field(
            ...,
            title="HTTP Method",
            description=("The HTTP method to use for the request."),
        ),
    ]
