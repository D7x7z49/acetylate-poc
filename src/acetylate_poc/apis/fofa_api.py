import base64

from acetylate_poc.schemas.http_request import RequestsSchema
from acetylate_poc.utils.requester import api_request_handler
from acetylate_poc.utils.validators import validate_api_key, validate_api_version, validate_base_url


class FofaAPI:

    VALID_API_VERSIONS = {'v1'}

    def __init__(self, api_key: str, base_url: str = 'https://fofa.info', api_version: str = 'v1') -> None:
        self.base_url = validate_base_url(base_url)
        self.api_key = validate_api_key(api_key)
        self.api_version = validate_api_version(api_version, self.VALID_API_VERSIONS)

    
    @api_request_handler()
    def search_all(self, query: str , page: int, size: int, fields: list[str] = None, full: bool = False):

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
            "qbase64": base64.b64encode(query.encode('utf-8')).decode('utf-8'),
            "fields": fields,
            "page": page,
            "size": size,
            "full": full
        }

        return RequestsSchema(method=method, url=url, params=params)

