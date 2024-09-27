from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class CTISearchEngineTarget(BaseModel):
    target_type: Annotated[
        Literal["network", "CTI SearchEngine"],
        Field(
            ...,
            title="Target Type",
            description=("The type of target, such as a network space or specific IP address."),
        ),
    ]
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
