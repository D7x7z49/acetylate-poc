from typing import Any, Callable, Dict, Type


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
