from urllib.parse import urlparse


def validate_api_key(api_key: str) -> str:
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("API Key must be a non-empty string.")
    return api_key


def validate_base_url(base_url: str) -> str:
    parsed_url = urlparse(base_url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValueError(f"Invalid Base URL: {base_url}")
    return base_url


def validate_api_version(api_version: str, valid_versions: set) -> str:
    if api_version not in valid_versions:
        raise ValueError(f"Invalid API version: {api_version}. Allowed versions: {valid_versions}")
    return api_version
