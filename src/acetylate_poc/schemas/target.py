from __future__ import annotations
from typing import Optional, List, Union, Annotated
from dataclasses import dataclass

@dataclass
class NetworkTarget:
    engine: Annotated[str, "The name of the network space search engine used to identify the target, such as Shodan or Censys."]
    query: Annotated[str, "The search query used with the search engine to locate potential targets or services."]
    port: Optional[Annotated[int, "Optional port number for the target. If not specified, all relevant ports are considered for the POC."]] = None
    path: Optional[Annotated[str, "Optional web path to include in the request. If not specified, the target is used without modification."]] = None


@dataclass
class Target:
    type: Annotated[str, "Specifies the type of target. 'network' indicates the use of a network space search engine and query to identify the target."]
    network: Optional[NetworkTarget] = None

    def __post_init__(self):
        if self.type == 'network' and self.network is None:
            raise ValueError("When type is 'network', 'network' field must be provided.")
        if self.type != 'network' and self.network is not None:
            raise ValueError("When type is not 'network', 'network' field should be None.")
