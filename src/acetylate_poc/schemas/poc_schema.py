from __future__ import annotations

from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from acetylate_poc.schemas.payload import (
    Payload,
)
from acetylate_poc.schemas.target import Target


class Description(BaseModel):
    title: Annotated[
        str,
        Field(
            ...,
            title="Title",
            description=("A brief title summarizing the content of the description."),
        ),
    ]
    content: Annotated[
        str,
        Field(
            ...,
            title="Content",
            description=(
                "A detailed narrative explaining the POC, "
                "including its purpose, potential impact, and any relevant technical details."
            ),
        ),
    ]
    references: Annotated[
        Optional[list[str]],
        Field(
            None,
            title="References",
            description=(
                "Optional array of references supporting the description, "
                "such as links to reports, articles, or other documentation."
            ),
        ),
    ]


class Metadata(BaseModel):
    authors: Annotated[
        list[str],
        Field(
            ...,
            title="Authors",
            description=(
                "An array listing the authors of the POC, " "providing credit to those who developed or documented it."
            ),
        ),
    ]
    descriptions: Annotated[
        list[Description],
        Field(
            ...,
            title="Descriptions",
            description=(
                "An array of descriptive sections providing context and details about the POC. "
                "Each description includes a title and content, with optional references."
            ),
        ),
    ]
    tags: Annotated[
        list[str],
        Field(
            ...,
            title="Tags",
            description=("An array of tags used to categorize and provide searchable attributes for the POC."),
        ),
    ]
    cve: Annotated[
        Optional[str | list[str]],
        Field(
            None,
            title="CVE",
            description=("Optional array of CVE identifiers that relate the POC to specific known vulnerabilities."),
        ),
    ]


class Assertion(BaseModel):
    condition: Annotated[
        str,
        Field(
            ...,
            title="Condition",
            description=("The type of condition to validate, " 'such as "status_code" or "response_body_contains".'),
        ),
    ]
    value: Annotated[
        str,
        Field(
            ...,
            title="Value",
            description=("The expected result or condition to check for in the POC's response."),
        ),
    ]
    message: Annotated[
        str,
        Field(
            None,
            title="Message",
            description=(
                "An optional message to display if the assertion fails, "
                "providing context or details about the failure."
            ),
        ),
    ]


class PocSchema(BaseModel):
    version: Annotated[
        str,
        Field(
            ...,
            title="Version",
            description=(
                "Indicates the version of the POC file format. "
                "This helps in managing and validating schema compatibility."
            ),
        ),
    ]
    metadata: Annotated[
        Metadata,
        Field(
            ...,
            title="Metadata",
            description=(
                "Metadata providing additional context about the POC, "
                "including authorship, descriptive information, related CVEs, and categorization tags."
            ),
        ),
    ]
    target: Annotated[
        Target,
        Field(
            ...,
            title="Target",
            description=(
                "Specification of the target for the POC. "
                "The structure depends on the type of target, "
                "such as network-based search engine queries."
            ),
        ),
    ]
    payload: Annotated[
        Payload,
        Field(
            ...,
            title="Payload",
            description=(
                "The payload used for the POC, which varies based on the protocol and type of data being sent."
            ),
        ),
    ]
    assertions: Annotated[
        list[Assertion],
        Field(
            ...,
            title="Assertions",
            description=(
                "A list of assertions to validate the POC's expected outcomes. "
                "Each assertion includes a condition to check and the expected value."
            ),
        ),
    ]

    model_config = ConfigDict(json_schema_extra={"title": "PoC Schema"})


if __name__ == "__main__":
    import json

    PocSchema.model_json_schema()

    print(json.dumps(PocSchema.model_json_schema(), indent=2))
