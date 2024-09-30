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
    kwargs = {'help': option_details.arg_help}
    match option_details.arg_type:
        case "str":
            kwargs['type'] = str  # Set type to string
        case "bool":
            kwargs['action'] = 'store_true'  # Boolean flag behavior
    if is_required:
        kwargs['required'] = True  # Mark as required if necessary

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
            group = parser.add_mutually_exclusive_group(required=True)  # Create a group for mutually exclusive options
            for o in opt:
                option_details = config.options[o]
                add_argument_to_parser(group, o, option_details)  # Add to the group
                required_args.append(o)
        else:
            option_details = config.options[opt]
            add_argument_to_parser(parser, opt, option_details, is_required=True)  # Add required argument
            required_args.append(opt)

    # Process optional arguments that are not required
    for opt, option_details in config.options.items():
        if opt not in required_args:
            add_argument_to_parser(parser, opt, option_details)  # Add optional argument

    return parser
