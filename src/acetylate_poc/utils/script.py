import argparse

from acetylate_poc.schemas.cli_args import CommandArgsSchema


def add_argument_to_parser(parser, arg_name, option_details, is_required=False):
    """
    Adds a command-line argument to the specified parser.

    Parameters:
        parser (argparse.ArgumentParser): The parser to which the argument is added.
        arg_name (str): The name of the argument.
        option_details (ArgOptionDetails): The details associated with the argument.
        is_required (bool): Indicates whether the argument is mandatory.

    This function constructs the long and short names for the argument,
    sets the appropriate type or action based on the argument's type,
    and adds it to the parser.
    """

    long_name = f"--{arg_name}"
    short_name = f"-{option_details.short_name}" if option_details.short_name else None

    # Prepare keyword arguments for the argument
    kwargs = {"help": option_details.arg_help}
    match option_details.arg_type:
        case "str":
            kwargs["type"] = str  # Set type to string
        case "bool":
            kwargs["action"] = "store_true"  # Boolean flag behavior
    if is_required:
        kwargs["required"] = True  # Mark as required if necessary

    # Add the argument to the parser with or without the short name
    if short_name:
        parser.add_argument(short_name, long_name, **kwargs)
    else:
        parser.add_argument(long_name, **kwargs)


def build_argparse(config: dict | CommandArgsSchema) -> argparse.ArgumentParser:
    """
    Constructs an ArgumentParser based on the provided configuration.

    Parameters:
        config (dict | CommandArgsSchema): The configuration dict or schema object.

    Returns:
        argparse.ArgumentParser: The configured argument parser.

    This function initializes the parser, adds required arguments (handling
    mutually exclusive groups where applicable), and includes optional arguments
    that are not required.
    """

    # If the config is a dictionary, validate and convert it to a schema object
    if isinstance(config, dict):
        config = CommandArgsSchema(**config)

    parser = argparse.ArgumentParser(description=config.description)
    required_args = []

    # Process required arguments
    for opt in config.required:
        if isinstance(opt, list):
            # Create a group for mutually exclusive options
            group = parser.add_mutually_exclusive_group(required=True)
            for o in opt:
                option_details = config.options[o]
                add_argument_to_parser(group, o, option_details)
                required_args.append(o)
        else:
            option_details = config.options[opt]
            add_argument_to_parser(parser, opt, option_details, is_required=True)
            required_args.append(opt)

    # Process optional arguments that are not required
    for opt, option_details in config.options.items():
        if opt not in required_args:
            add_argument_to_parser(parser, opt, option_details)

    return parser


if __name__ == "__main__":
    # Example configuration for the argument parser
    config_data = {
        "description": "This is an example command-line interface for demonstration.",
        "required": ["input", "output"],
        "options": {
            "input": {"short_name": "i", "arg_help": "Input file path", "arg_type": "str"},
            "output": {"short_name": "o", "arg_help": "Output file path", "arg_type": "str"},
            "verbose": {"short_name": "v", "arg_help": "Enable verbose mode", "arg_type": "bool"},
            "overwrite": {"short_name": None, "arg_help": "Overwrite existing files", "arg_type": "bool"},
        },
    }

    parser = build_argparse(config_data)
    args = parser.parse_args(["--help"])
