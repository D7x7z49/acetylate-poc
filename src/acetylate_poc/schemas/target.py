from __future__ import annotations

from typing import Annotated, Optional

from pydantic import BaseModel, Field, model_validator


class CTISearchEngineTarget(BaseModel):
    engine: Annotated[
        str,
        Field(
            ...,
            title="Cyber Threat Intelligence (CTI) Search Engine",
            description=("The name of the CTI search engine used to identify the target, " "such as Shodan or Censys."),
        ),
    ]
    query: Annotated[
        str,
        Field(
            ...,
            title="Search Query",
            description=("The search query used with the search engine to locate potential targets or services."),
        ),
    ]


class Target(BaseModel):
    type: Annotated[
        str,
        Field(
            ...,
            title="Target Type",
            description=(
                "Specifies the type of target. "
                "`network` indicates the use of a network space search engine and query to identify the target."
            ),
        ),
    ]
    network: Annotated[
        Optional[CTISearchEngineTarget],
        Field(
            default=None,
            title="Network Target",
            description=(
                "If the target type is `network`, provide the details of the network space search engine and query."
            ),
        ),
    ]

    @classmethod
    @model_validator(mode="before")
    def validate_network(cls, values):
        target_type = values.get("type")
        network = values.get("network")

        if target_type == "network" and network is None:
            raise ValueError("When type is 'network', 'network' field must be provided.")
        if target_type != "network" and network is not None:
            raise ValueError("When type is not 'network', 'network' field should be None.")

        return values
