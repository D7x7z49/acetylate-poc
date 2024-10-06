from acetylate_poc.schemas.http_request import RequestsSchema
from acetylate_poc.utils.manage import GeneralToolsBox
from acetylate_poc.utils.requester import api_request_handler
from acetylate_poc.utils.validators import validate_api_key, validate_api_version, validate_base_url

str_to_base64 = GeneralToolsBox.base64_str

class FofaAPI:

    VALID_API_VERSIONS = {'v1'}

    def __init__(self, api_key: str, base_url: str = 'https://fofa.info', api_version: str = 'v1') -> None:
        self.base_url = validate_base_url(base_url)
        self.api_key = validate_api_key(api_key)
        self.api_version = validate_api_version(api_version, self.VALID_API_VERSIONS)

    
    @api_request_handler()
    def search_all(self, query: str , page: int, size: int, fields: list[str] = None, full: bool = False) -> dict:

        default_fields = [
            "ip", "port", "protocol", "country", "country_name", "region", "city", "longitude", "latitude",
            "as_number", "as_organization", "host", "domain", "os", "server", "icp", "title", "jarm",
            "header", "banner", "cert", "base_protocol", "link", "certs_issuer_org", "certs_issuer_cn",
            "certs_subject_org", "certs_subject_cn", "tls_ja3s", "tls_version"]
        fields = ",".join(fields) if fields else ",".join(default_fields)
        
        method = "GET"

        url = f"{self.base_url}/api/{self.api_version}/search/all"

        params = {
            "key": self.api_key,
            "qbase64": str_to_base64(query),
            "fields": fields,
            "page": page,
            "size": size,
            "full": full
        }

        return RequestsSchema(method=method, url=url, params=params)

    @api_request_handler()
    def search_stats(self, query: str, fields: list[str] = None) -> dict:

        default_fields = [
            "protocol", "domain", "port", "title", "os", "server", "country",
            "as_number", "as_organization", "asset_type", "fid", "icp"
        ]

        fields = ",".join(fields) if fields else ",".join(default_fields)
       
        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/search/stats"

        params = {
            "key": self.api_key,
            "qbase64": str_to_base64(query),
            "fields": fields
        }

        return RequestsSchema(method=method, url=url, params=params)
    
    @api_request_handler()
    def host_aggregation(self, host: str, detail: bool = False) -> dict:

        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/host/{host}"

        params = {
            "key": self.api_key,
            "detail": detail
        }

        return RequestsSchema(method=method, url=url, params=params)
    
    @api_request_handler()
    def account_info(self) -> dict:

        method = "GET"
        url = f"{self.base_url}/api/{self.api_version}/info/my"

        params = {
            "key": self.api_key
        }

        return RequestsSchema(method=method, url=url, params=params)
    
    @api_request_handler()
    def search_next(
        self, query: str, fields: list[str] = None, size: int = 100, next_id: str = None, full: bool = False
    ) -> dict:

        default_fields = [
            "ip", "port", "protocol", "country", "country_name", "region", "city", "longitude", "latitude",
            "as_number", "as_organization", "host", "domain", "os", "server", "icp", "title", "jarm",
            "header", "banner", "cert", "base_protocol", "link", "certs_issuer_org", "certs_issuer_cn",
            "certs_subject_org", "certs_subject_cn", "tls_ja3s", "tls_version"
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
            "full": full
        }

        return RequestsSchema(method=method, url=url, params=params)