"""Module from initializing Component Class"""

from functools import cached_property
from typing import Self

from .context import component_registry


class BaseComponent:
    def __init__(self, name=""):
        self.name = name
        component_registry.append(self)

    @classmethod
    def get_component_or_none(cls, name="", strict=False, **kw) -> Self | None:
        for component in component_registry:
            if (
                isinstance(component, cls)
                and (not strict or type(component) is cls)
                and (not name or name == component.name)
            ):
                return component
        return None

    @classmethod
    def get_cached_component_or_none(cls, name="", strict=False, **kw) -> cached_property[Self | None]:
        return cached_property(lambda _: cls.get_component_or_none(name=name, strict=strict, **kw))

    @classmethod
    def get_component(cls, name="", strict=False, **kw) -> Self:
        component = cls.get_component_or_none(name=name, strict=strict, **kw)
        if component is None:
            raise KeyError(f"No component of type '{cls.__name__}' found matching name='{name}'.")
        return component

    @classmethod
    def get_cached_component(cls, name="", strict=False, **kw) -> cached_property[Self]:
        return cached_property(lambda _: cls.get_component(name=name, strict=strict, **kw))
