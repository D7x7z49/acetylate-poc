from __future__ import annotations

from typing import Annotated, Any, Type

from pydantic import BaseModel, Field, ValidationError, model_validator

payload_registry: dict[str, Type[BaseModel]] = {}


def register_payload(payload_type: str):
    def wrapper(cls: Type[BaseModel]):
        payload_registry[payload_type] = cls
        return cls

    return wrapper


@register_payload("tcp")
class TcpPayload(BaseModel):
    source_port: Annotated[
        int,
        Field(
            ...,
            title="Source Port",
            description=("The source port number for the TCP connection."),
        ),
    ]
    destination_port: Annotated[
        int,
        Field(
            ...,
            title="Destination Port",
            description=("The destination port number for the TCP connection."),
        ),
    ]


@register_payload("udp")
class UdpPayload(BaseModel):
    pass


class Payload(BaseModel):
    payload_type: Annotated[
        str,
        Field(
            ...,
            title="Payload Type",
            description=("The type of payload, which determines the format and content of the payload data."),
        ),
    ]
    payload_data: Annotated[
        TcpPayload | UdpPayload | Any,
        Field(
            ...,
            title="Payload Data",
            description=("The actual payload data, formatted according to the specified payload_type."),
        ),
    ]

    @classmethod
    @model_validator(mode="before")
    def validate_payload_data(cls, values):
        payload_type = values.get("payload_type")
        payload_data = values.get("payload_data")

        if payload_type in payload_registry:
            expected_model = payload_registry[payload_type]
            if payload_data is not None:
                try:
                    validated_data = expected_model(**payload_data)
                    values["payload_data"] = validated_data
                except ValidationError as e:
                    raise ValueError(f"Invalid data for {payload_type}: {e}") from e
            else:
                raise ValueError(f"payload_data is required for {payload_type}")
        else:
            raise ValueError(f"Unknown payload_type: {payload_type}")

        return values
