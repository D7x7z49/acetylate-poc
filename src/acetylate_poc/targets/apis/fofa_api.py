"""
fofa_api.py

This module provides a Python client for interacting with the Fofa API, enabling users to perform various queries
such as searching, aggregating, and retrieving account information.

Classes:
    FofaAPI: A class that encapsulates the methods to interact with the Fofa API.

Usage:
    Initialize the FofaAPI class with a valid API key, and then call the desired methods to interact with the API.
"""

from acetylate_poc.targets.api_box import BaseAPI, api_request_handler
from acetylate_poc.utils.manage import GeneralToolsBox
from acetylate_poc.utils.validators import validate_api_key, validate_api_version

str_to_base64 = GeneralToolsBox.base64_str


class FofaAPI:
    """
    FofaAPI class to interact with the Fofa service.

    Attributes:
        VALID_API_VERSIONS (set): A set of valid API versions supported by the Fofa service.
        base_url (str): The base URL of the Fofa API.
        api_key (str): The API key for authentication.
        api_version (str): The version of the API being used.
    """

    base_url: str = r"https://fofa.info"
    VALID_API_VERSIONS = {"v1"}

    def __init__(self, api_key: str, api_version: str = "v1", requester: str = "requests") -> None:
        """
        Initialize the FofaAPI instance.

        Parameters:
            api_key (str): The API key for authenticating requests.
            api_version (str): The version of the API to use (default is "v1").
            requester (str): The HTTP library to use for requests (default is "requests").

        Raises:
            ValueError: If the API key or API version is invalid.
        """

        self.api_key = validate_api_key(api_key)
        self.api_version = validate_api_version(api_version, self.VALID_API_VERSIONS)
        self.requester = requester

    def send(self, method, url, params) -> dict:
        """
        Send an HTTP request to the Fofa API.

        Parameters:
            method (str): The HTTP method to use (e.g., "GET").
            url (str): The full URL of the API endpoint.
            params (dict): The parameters to include in the request.

        Returns:
            dict: The response from the Fofa API.
        """

        @api_request_handler(self.requester)
        def func():
            return BaseAPI(method=method, url=url, params=params)

        return func()

    def search_all(self, query: str, page: int, size: int, fields: list[str] = None, full: bool = False) -> dict:
        """
        Perform a search query on all data.

        Parameters:
            query (str): The search query to be executed.
            page (int): The page number for pagination (0-indexed).
            size (int): The number of results to return per page (max 1000).
            fields (list[str], optional): The specific fields to return (default is predefined fields).
            full (bool, optional): Whether to retrieve all data (default is False).

        Returns:
            dict: The response from the Fofa API containing search results.
        """
        # Default fields if none are specified
        default_fields = [
            "ip",
            "port",
            "protocol",
            "country",
            "country_name",
            "region",
            "city",
            "longitude",
            "latitude",
            "as_number",
            "as_organization",
            "host",
            "domain",
            "os",
            "server",
            "icp",
            "title",
            "jarm",
            "header",
            "banner",
            "cert",
            "base_protocol",
            "link",
            "certs_issuer_org",
            "certs_issuer_cn",
            "certs_subject_org",
            "certs_subject_cn",
            "tls_ja3s",
            "tls_version",
        ]
        fields = ",".join(fields) if fields else ",".join(default_fields)

        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/search/all"

        params = {
            "key": self.api_key,
            "qbase64": str_to_base64(query),
            "fields": fields,
            "page": page,
            "size": size,
            "full": full,
        }

        return self.send(method=method, url=url, params=params)

    def search_stats(self, query: str, fields: list[str] = None) -> dict:
        """
        Retrieve statistics based on a search query.

        Parameters:
            query (str): The search query for which to retrieve statistics.
            fields (list[str], optional): The specific fields for statistics (default is predefined fields).

        Returns:
            dict: The response from the Fofa API containing statistics.
        """
        default_fields = [
            "protocol",
            "domain",
            "port",
            "title",
            "os",
            "server",
            "country",
            "as_number",
            "as_organization",
            "asset_type",
            "fid",
            "icp",
        ]

        fields = ",".join(fields) if fields else ",".join(default_fields)

        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/search/stats"

        params = {"key": self.api_key, "qbase64": str_to_base64(query), "fields": fields}

        return self.send(method=method, url=url, params=params)

    def host_aggregation(self, host: str, detail: bool = False) -> dict:
        """
        Retrieve aggregation information for a specific host.

        Parameters:
            host (str): The host name, typically an IP address.
            detail (bool, optional): Whether to display port details (default is False).

        Returns:
            dict: The response from the Fofa API containing host aggregation information.
        """
        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/host/{host}"

        params = {"key": self.api_key, "detail": detail}

        return self.send(method=method, url=url, params=params)

    def account_info(self) -> dict:
        """
        Retrieve current account information.

        Returns:
            dict: The response from the Fofa API containing account information.
        """
        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/info/my"

        params = {"key": self.api_key}

        return self.send(method=method, url=url, params=params)

    def search_next(
        self, query: str, fields: list[str] = None, size: int = 100, next_id: str = None, full: bool = False
    ) -> dict:
        """
        Continuously fetch data for the same search query using a pagination ID.

        Parameters:
            query (str): The search query to be executed.
            fields (list[str], optional): The specific fields to return (default is predefined fields).
            size (int, optional): The number of results per page (default is 100).
            next_id (str, optional): The pagination ID for the next set of results (default is None).
            full (bool, optional): Whether to search all data (default is False).

        Returns:
            dict: The response from the Fofa API containing the next page of search results.
        """
        default_fields = [
            "ip",
            "port",
            "protocol",
            "country",
            "country_name",
            "region",
            "city",
            "longitude",
            "latitude",
            "as_number",
            "as_organization",
            "host",
            "domain",
            "os",
            "server",
            "icp",
            "title",
            "jarm",
            "header",
            "banner",
            "cert",
            "base_protocol",
            "link",
            "certs_issuer_org",
            "certs_issuer_cn",
            "certs_subject_org",
            "certs_subject_cn",
            "tls_ja3s",
            "tls_version",
        ]

        fields = ",".join(fields) if fields else ",".join(default_fields)

        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/search/next"

        params = {
            "key": self.api_key,
            "qbase64": str_to_base64(query),
            "fields": fields,
            "size": size,
            "next": next_id,
            "full": full,
        }

        return self.send(method=method, url=url, params=params)
