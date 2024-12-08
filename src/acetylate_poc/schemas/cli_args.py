from __future__ import annotations

from typing import Annotated, Dict, Literal, Optional

from pydantic import BaseModel, Field, model_validator


class ArgOptionDetails(BaseModel):
    """
    Represents the details of a command-line argument option.

    Attributes:
        short_name (Optional[str]):
            The abbreviated name for the argument, typically a single character.
        arg_type (Literal["str", "bool"]):
            The type of argument, which can be a string or a boolean.
        arg_help (str):
            A brief explanation of what the argument does.
    """

    short_name: Annotated[
        Optional[str],
        Field(
            None, title="Short Name", description="The abbreviated name for the argument, typically a single character."
        ),
    ]
    arg_type: Annotated[
        Literal["str", "bool"],
        Field(None, title="Argument Type", description="The type of argument, which can be a string or a number."),
    ] = "str"
    arg_help: Annotated[
        str, Field(..., title="Argument Help", description="A brief explanation of what the argument does.")
    ]


class CommandArgsSchema(BaseModel):
    """
    Defines the schema for command-line arguments for a specific command.

    Attributes:
        description (str):
            A concise overview of the command's purpose and functionality.
        required (list[str | list[str]]):
            A list of arguments that must be provided when invoking the command.
            Each item can be a string or a list of mutually exclusive options.
        options (Dict[str, ArgOptionDetails]):
            A dictionary of optional arguments available for the command,
            with argument names as keys and their details (short form and help) as values.
    """

    description: Annotated[
        str,
        Field(..., title="Description", description="A concise overview of the command's purpose and functionality."),
    ]
    required: Annotated[
        list[str | list[str]],
        Field(
            None,
            title="Required Arguments",
            description=(
                "A list of arguments that must be provided when invoking the command. "
                "Each item can be a string or a list of mutually exclusive options."
            ),
        ),
    ]
    options: Annotated[
        Dict[str, ArgOptionDetails],
        Field(
            ...,
            title="Options",
            description=(
                "A dictionary of optional arguments available for the command, "
                "with argument names as keys and their details (short form and help) as values."
            ),
        ),
    ]

    @model_validator(mode="after")
    def validate_required(self) -> CommandArgsSchema:
        """
        Validates that all required arguments are defined in the options.

        Raises:
            ValueError: If any required argument is not found in the options.

        This method checks both direct required arguments and mutually exclusive options,
        ensuring that all specified required arguments are present in the options dictionary.
        """
        required = self.required
        options = self.options
        for arg in required:
            if isinstance(arg, list):
                for opt in arg:
                    if (opt not in options) or (opt in required):
                        raise ValueError(f"Required argument '{opt}' not found in options.")
            elif arg not in options:
                raise ValueError(f"Required argument '{arg}' not found in options.")

        return self
