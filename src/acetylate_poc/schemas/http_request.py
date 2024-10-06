from __future__ import annotations

from typing import Annotated, Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class HttpBaseSchema(BaseModel):
    method: Annotated[
        Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'],
        Field(..., description="The HTTP method to use for the request.")
    ]
    url: Annotated[str, Field(..., description="The URL to send the request to.")]
    headers: Optional[Dict[str, str]] = Field(None, description="Headers to include in the request.")
    params: Optional[Dict[str, Any]] = Field(None, description="Query parameters for the request.")
    data: Optional[Dict[str, Any]] = Field(None, description="Data to send in the body of the request.")
    timeout: Optional[float] = Field(7.0, description="Timeout for the request in seconds.")
    cookies: Optional[Dict[str, str]] = Field(None, description="Cookies to send with the request.")
    auth: Optional[Dict[str, str]] = Field(None, description="Authentication credentials.")
    verify: Optional[bool] = Field(True, description="Whether to verify SSL certificates.")
    proxies: Optional[Dict[str, str]] = Field(None, description="Proxy settings for the request.")


class RequestsSchema(HttpBaseSchema):
    pass


class HTTPXSchema(HttpBaseSchema):
    pass


class AIOHTTPSchema(HttpBaseSchema):
    pass


