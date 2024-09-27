"""
fetch.py

This module provides utility functions for extracting data from various data sources.
The primary purpose of these functions is to facilitate data retrieval and processing.

Functions:
- <function_name_1>: Brief description of what this function does.
- <function_name_2>: Brief description of what this function does.
- <function_name_3>: Brief description of what this function does.
"""


import csv
import json
import re
from pathlib import Path


def separate_file_iterator(inputfile, outputfile, regex_pattern):
    pattern = re.compile(regex_pattern)

    with open(inputfile, "r") as infile, open(outputfile, "w") as outfile:
        for line in infile:
            target = line.strip()
            if pattern.match(target):
                yield target
            else:
                outfile.write(f"{target}\n")


def extract_file_iterator(file_path, filter_keys):
    path = Path(file_path)
    file_extension = path.suffix

    supported_extensions = ['.ndjson', '.json', '.csv']

    if file_extension in ['.ndjson', '.json']:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    yield {k: data[k] for k in filter_keys if k in data}
                except json.JSONDecodeError:
                    continue

    elif file_extension == '.csv':
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield {k: row[k] for k in filter_keys if k in row}

    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}. Supported types are {', '.join(supported_extensions)}."
        )
