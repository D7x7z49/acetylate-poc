import base64
import re
import time
from functools import wraps
from typing import Any, Callable, Dict, Type
from urllib.parse import ParseResult, urlparse, urlunparse


class Registry:
    def __init__(self, initial_registry: Dict[str, Callable | Type] = None):
        self._registry: Dict[str, Callable | Type] = initial_registry if initial_registry is not None else {}

    def register(self, key: str) -> Callable:
        if not isinstance(key, str):
            raise ValueError(f"Key '{key}' is not a valid identifier.")
        
        def decorator(obj: Callable | Type):
            if key in self._registry:
                raise ValueError(f"Key '{key}' is already registered.")
            
            if not callable(obj) and not isinstance(obj, type):
                raise TypeError(f"Object must be callable or a class. Got {type(obj)}.")
            
            self._registry[key] = obj
            return obj
        return decorator
    
    def dispatch(self, key: str, *args: Any, **kwargs: Any) -> Any:
        if key not in self._registry:
            raise KeyError(f"Key '{key}' is not found in registry.")
        
        obj = self._registry[key]
        
        if any(not isinstance(arg, (str, int)) for arg in args):
            raise ValueError("All arguments must be strings or integers.")
        
        if isinstance(obj, type):
            return obj(*args, **kwargs)
        return obj(*args, **kwargs)

    def get_all_keys(self) -> list:
        return list(self._registry.keys())

    def __repr__(self) -> str:
        return f"Registry({self._registry})"
    

class GeneralToolsBox:

    @staticmethod
    def timeit(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            result = await func(*args, **kwargs)
            end_time = time.monotonic()
            print(f"Execution time: {end_time - start_time:.2f} seconds")
            return result
        return wrapper
    
    @staticmethod
    def base64_str(s: str | bytes, encode: str = "utf-8") -> str:
        
        if isinstance(s, bytes):
            return base64.b64encode(s).decode(encode)
        elif isinstance(s, str):
            return base64.b64encode(s.encode(encode)).decode(encode)
        else:
            raise TypeError("Input must be a string or bytes")
    
    @staticmethod
    def fix_base_url(host: str, protocol: str, ip: str, domain: str, port):
        if "://" in host:
            protocol_split = host.split("://", 1)
            scheme = protocol_split[0]
            netloc = protocol_split[1]
        else:
            scheme = protocol
            netloc = host
        
        if ":" in netloc:
            netloc_split = netloc.split(":", 1)
            base_host = netloc_split[0]
            port_from_host = netloc_split[1]
        else:
            base_host = netloc
            port_from_host = port

        if base_host and port_from_host:
            return urlunparse((scheme, f"{base_host}:{port_from_host}", '', '', '', ''))
        
        final_netloc = f"{domain if domain else ip}:{port_from_host}"
        return urlunparse((scheme, final_netloc, '', '', '', ''))


if __name__ == "__main__":

    registry = Registry()

    @registry.register('greet')
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    @registry.register('person')
    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def __str__(self) -> str:
            return f"{self.name}, {self.age} years old"

    print(registry.dispatch('greet', 'Alice'))
    print(registry.get_all_keys())

    try:
        registry.dispatch('non_existent')
    except KeyError as e:
        print(e)

    try:
        registry.dispatch('greet', 42)
    except ValueError as e:
        print(e)
