from __future__ import annotations
from typing import List, Optional, Annotated
from dataclasses import dataclass
from acetylate_poc.schemas import Target, NetworkTarget
from acetylate_poc.schemas import Payload, HttpPayload, TcpPayload

@dataclass
class Description:
    title: Annotated[str, "A brief title summarizing the content of the description."]
    content: Annotated[str, "A detailed narrative explaining the POC, including its purpose, potential impact, and any relevant technical details."]
    references: Optional[Annotated[List[str], "Optional array of references supporting the description, such as links to reports, articles, or other documentation."]] = None

@dataclass
class Metadata:
    authors: Annotated[List[Annotated[str, "Name of an individual who contributed to the creation of the POC."]], "An array listing the authors of the POC, providing credit to those who developed or documented it."]
    descriptions: Annotated[List[Description], "An array of descriptive sections providing context and details about the POC. Each description includes a title and content, with optional references."]
    tags: Annotated[List[Annotated[str, "Keywords or labels that categorize the POC, making it easier to search and filter POCs based on their characteristics."]], "An array of tags used to categorize and provide searchable attributes for the POC."]
    cve: Optional[Annotated[List[Annotated[str, "A list of Common Vulnerabilities and Exposures (CVE) identifiers related to the POC."]], "Optional array of CVE identifiers that relate the POC to specific known vulnerabilities."]] = None

@dataclass
class Assertion:
    condition: Annotated[str, "The type of condition to validate, such as 'status_code' or 'response_body_contains'."]
    value: Annotated[str, "The expected result or condition to check for in the POC's response."]
    message: Optional[Annotated[str, "An optional message to display if the assertion fails, providing context or details about the failure."]] = None

@dataclass
class POCSchema:
    version: Annotated[str, "Indicates the version of the POC file format. This helps in managing and validating schema compatibility."]
    metadata: Annotated[Metadata, "Metadata providing additional context about the POC, including authorship, descriptive information, related CVEs, and categorization tags."]
    target: Annotated[Target, "Specification of the target for the POC. The structure depends on the type of target, such as network-based search engine queries."]
    payload: Annotated[Payload, "The payload used for the POC, which varies based on the protocol and type of data being sent."]
    assertions: Annotated[List[Assertion], "A list of assertions to validate the POC's expected outcomes. Each assertion includes a condition to check and the expected value."]

