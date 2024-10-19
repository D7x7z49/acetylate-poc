from acetylate_poc.targets.api_box import BaseAPI, api_request_handler


class IpinfoAPI:
    """
    Wrapper for the ipinfo.io API.

    Provides methods to interact with the IP information service provided by ipinfo.io.
    """

    base_url = r"https://ipinfo.io"

    def __init__(self, tonken: str, requester: str = "requests") -> None:
        """
        Initialize the IpinfoAPI with an API token and a requester.

        Args:
            tonken (str): The API token required for authenticating requests to ipinfo.io.
            requester (str): The HTTP library to use for requests. Default is 'requests'.
        """
        self.requester = requester
        self.tonken = tonken

    def ipinfo(self, ip: str) -> dict:
        """
        Retrieve information about a specific IP address.

        This method makes a GET request to ipinfo.io to fetch details such as location, ASN, and hostname
        for the given IP address.

        Args:
            ip (str): The IP address (IPv4 or IPv6) to retrieve information for.

        Returns:
            dict: A dictionary containing details about the IP address such as city, region, country, ASN, etc.
        """
        @api_request_handler(self.requester)
        def func():
            return BaseAPI(
                method="GET",
                url=f"{self.base_url}/{ip}/json",
                params={
                    "token": self.tonken
                }
            )

        return func()


class HostAPI:
    """
    Wrapper for the host.io API.

    Provides methods to interact with host.io's services, including DNS lookup, related domains, and
    web information for domains.
    """

    base_url = r"https://host.io"
    SUPPORTED_FIELDS = {
        "ip", "ns", "mx", "asn", "backlinks", "redirects", "adsense",
        "facebook", "twitter", "instagram", "gtm", "googleanalytics", "email"
    }

    def __init__(self, tonken: str, limit: int = 5, page: int = 0, requester: str = "requests") -> None:
        """
        Initialize the HostAPI with an API token, requester, and default query parameters.

        Args:
            tonken (str): The API token required for authenticating requests to host.io.
            limit (int): The number of results to retrieve per page. Default is 5.
            page (int): The page of results to retrieve. Default is 0.
            requester (str): The HTTP library to use for requests. Default is 'requests'.
        """
        self.requester = requester
        self.tonken = tonken
        self.limit = limit
        self.page = page

    def web_host(self, host: str) -> dict:
        """
        Retrieve web information about a specific host (domain).

        This method makes a GET request to host.io to retrieve web-related information about a given host,
        including domain reputation, traffic, and social media presence.

        Args:
            host (str): The domain or host to retrieve web information for.

        Returns:
            dict: A dictionary containing web-related details about the host.
        """
        @api_request_handler(self.requester)
        def func():
            return BaseAPI(
                method="GET",
                url=f"{self.base_url}/api/web/{host}",
                params={
                    "token": self.tonken,
                    "limit": self.limit,
                    "page": self.page
                }
            )

        return func()

    def dns_host(self, host: str) -> dict:
        """
        Retrieve DNS information about a specific host (domain).

        This method makes a GET request to host.io to retrieve DNS-related information such as A, AAAA,
        NS, MX, and other DNS records for the given host.

        Args:
            host (str): The domain or host to retrieve DNS information for.

        Returns:
            dict: A dictionary containing DNS records related to the host.
        """
        @api_request_handler(self.requester)
        def func():
            return BaseAPI(
                method="GET",
                url=f"{self.base_url}/api/dns/{host}",
                params={
                    "token": self.tonken,
                    "limit": self.limit,
                    "page": self.page
                }
            )

        return func()

    def related_host(self, host: str) -> dict:
        """
        Retrieve related domains for a specific host (domain).

        This method makes a GET request to host.io to retrieve domains that are related to the given host,
        such as shared DNS records, backlinks, or redirects.

        Args:
            host (str): The domain or host to retrieve related domains for.

        Returns:
            dict: A dictionary containing related domains for the given host.
        """
        @api_request_handler(self.requester)
        def func():
            return BaseAPI(
                method="GET",
                url=f"{self.base_url}/api/related/{host}",
                params={
                    "token": self.tonken,
                    "limit": self.limit,
                    "page": self.page
                }
            )

        return func()

    def full_host(self, host: str) -> dict:
        """
        Retrieve comprehensive information about a specific host (domain).

        This method makes a GET request to host.io to retrieve all available data about the given host,
        including DNS records, backlinks, redirects, and other relevant details.

        Args:
            host (str): The domain or host to retrieve full information for.

        Returns:
            dict: A dictionary containing full information about the host.
        """
        @api_request_handler(self.requester)
        def func():
            return BaseAPI(
                method="GET",
                url=f"{self.base_url}/api/full/{host}",
                params={
                    "token": self.tonken,
                    "limit": self.limit,
                    "page": self.page
                }
            )

        return func()

    def domains_host(self, field: str, value: str) -> dict:
        """
        Retrieve domains associated with a specific field and value.

        This method makes a GET request to host.io to retrieve domains associated with 
        the specified field (e.g., IP address, ASN, backlinks) and the corresponding value. 
        Supported fields are: 
            ip, ns, mx, asn, backlinks, redirects, adsense, facebook, twitter, instagram, gtm, googleanalytics, email.

        Args:
            field (str): The field to query by (e.g., 'ip', 'ns', 'asn').
            value (str): The value associated with the field (e.g., '8.8.8.8' for 'ip').

        Returns:
            dict: A dictionary containing domains associated with the given field and value.

        Raises:
            ValueError: If the field is not one of the supported fields.
        """
        if field not in self.SUPPORTED_FIELDS:
            raise ValueError(
                f"Field '{field}' is not supported. Supported fields are: {', '.join(self.SUPPORTED_FIELDS)}"
            )

        @api_request_handler(self.requester)
        def func():
            return BaseAPI(
                method="GET",
                url=f"{self.base_url}/api/domains/{field}/{value}",
                params={
                    "token": self.tonken,
                    "limit": self.limit,
                    "page": self.page
                }
            )

        return func()
