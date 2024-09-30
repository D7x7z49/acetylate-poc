from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from acetylate_poc.schemas.payload import HttpPayload, TcpPayload, UdpPayload
from acetylate_poc.schemas.target import CTISearchEngineTarget


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
            min_length=1,
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
            min_length=1,
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
        Literal["1.0"],
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
        CTISearchEngineTarget,
        Field(
            ...,
            title="Target",
            description=(
                "Specification of the target for the POC. "
                "The structure depends on the type of target, "
                "such as network-based search engine queries."
            ),
            discriminator="target_type",
        ),
    ]
    payload: Annotated[
        TcpPayload | UdpPayload | HttpPayload,
        Field(
            ...,
            title="Payload",
            description=(
                "The payload used for the POC, which varies based on the protocol and type of data being sent."
            ),
            discriminator="payload_type",
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
            min_length=1,
        ),
    ]

    model_config = ConfigDict(json_schema_extra={"title": "PoC Schema"})


if __name__ == "__main__":
    import json

    schema = PocSchema.model_json_schema()

    with open("example\\v1.poc-schema.json5", "w") as json_file:
        json.dump(schema, json_file, indent=2)
