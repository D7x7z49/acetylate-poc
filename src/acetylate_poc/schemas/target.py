from __future__ import annotations

from typing import Annotated, Any, Type

from pydantic import BaseModel, Field, ValidationError, model_validator

target_registry: dict[str, Type[BaseModel]] = {}


def register_target(target_type: str):
    def wrapper(cls: Type[BaseModel]):
        target_registry[target_type] = cls
        return cls

    return wrapper


@register_target("network")
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
    target_data: Annotated[
        CTISearchEngineTarget | Any,
        Field(
            ...,
            title="Target Data",
            description=(
                "The details of the target data, formatted according to the target type."
            ),
        ),
    ]

    @classmethod
    @model_validator(mode="before")
    def validate_target_data(cls, values):
        target_type = values.get("type")
        target_data = values.get("target_data")

        if target_type in target_registry:
            expected_model = target_registry[target_type]
            if target_data is not None:
                try:
                    validated_data = expected_model(**target_data)
                    values["target_data"] = validated_data
                except ValidationError as e:
                    raise ValueError(f"Invalid data for {target_type}: {e}") from e
            else:
                raise ValueError(f"target_data is required for {target_type}")
        else:
            raise ValueError(f"Unknown target_type: {target_type}")

        return values
