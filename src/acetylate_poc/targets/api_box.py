from __future__ import annotations

from abc import ABC, abstractmethod
from functools import wraps
from typing import Annotated, Any, Dict, Literal, Optional, Type

import requests
from pydantic import BaseModel, Field, HttpUrl
from requests import Response

from acetylate_poc.utils.manage import Registry

_requester_registry = Registry()



class BaseAPI(BaseModel):
    url: Annotated[HttpUrl, Field(..., description="The URL of the API endpoint.")]
    method: Annotated[
        Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'],
        Field(..., description="The HTTP method to use for the request.")
    ]
    params: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="Query parameters for the request.")
    ] = None
    headers: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="Headers to include in the request.")
    ] = None
    data: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="Data to send in the body of the request.")
    ] = None
    auth: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="Authentication credentials.")
    ] = None
    cookies: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="Cookies to send with the request.")
    ] = None
    proxies: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="Proxy settings for the request.")
    ] = None
    verify: Annotated[
        Optional[bool],
        Field(True, description="Whether to verify SSL certificates.")
    ] = True
    timeout: Annotated[
        Optional[float],
        Field(7.0, description="Timeout for the request in seconds.")
    ] = 7.0



class AbstractRequester(ABC):
    @abstractmethod
    def send_request(self, **kwargs):
        pass


@_requester_registry.register("requests")
class RequestsRequester(AbstractRequester):
    def send_request(self, is_json=False, **kwargs):

        method = kwargs.pop('method', None)
        if is_json:
            kwargs['json'] = kwargs.pop('data', None)

        request_methods = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "PATCH": requests.patch,
            "OPTIONS": requests.options,
            "HEAD": requests.head
        }

        if method not in request_methods:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response: Response = request_methods[method](**kwargs)
        return response.json()
    

@_requester_registry.register("httpx")
class HttpxRequester(AbstractRequester):
    def send_request(self, **kwargs):
        pass


@_requester_registry.register("aiohttp")
class AiohttpRequester(AbstractRequester):
    def send_request(self, **kwargs):
        pass


@_requester_registry.register("http.client")
class HttpClientRequester(AbstractRequester):
    def send_request(self, **kwargs):
        pass


def api_request_handler(requester_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> dict:
            requester: AbstractRequester = _requester_registry.dispatch(requester_type)
            http_args: dict | BaseModel = func(*args, **kwargs)
            if isinstance(http_args, BaseModel):
                http_args = http_args.model_dump(mode="json")
            return requester.send_request(**http_args)
        return wrapper
    return decorator


def api_request_register(key: str):
    def decorator(requester_cls: Type[AbstractRequester]):
        if not issubclass(requester_cls, AbstractRequester):
            raise TypeError(f"{requester_cls.__name__} must inherit from AbstractRequester.")
        return _requester_registry.register(key)(requester_cls)
    return decorator