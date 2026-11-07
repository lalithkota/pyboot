from typing import Generic, Self, TypeVar

_T = TypeVar("_T")


class Holder(Generic[_T]):
    """
    Useful holder tool for passing mutable object across functions.
    Define a Holder object like:
    ```python
    a_holder = Holder[int](123)
    ```
    or
    ```python
    a_holder = Holder[int]()
    a_holder.set(123)
    ```
    and get using
    ```python
    a_holder.get(default=456)
    ```
    """

    def __init__(self, value: _T | None = None):
        super().__init__()
        self.value: _T | None = value

    def get(self, default: _T | None = None) -> _T | None:
        if self.value is None:
            return default
        return self.value

    def set(self, value: _T | None) -> Self:
        self.value = value
        return self


class HolderNonNull(Generic[_T]):
    """
    Useful holder tool for passing mutable non-null object across functions.
    Define a HolderNonNull object like:
    ```python
    a_holder = HolderNonNull[int](123)
    ```
    and get using
    ```python
    a_holder.get()
    ```
    and set using
    ```python
    a_holder.set(456)
    ```
    """

    def __init__(self, value: _T):
        super().__init__()
        if value is None:
            raise ValueError("Holder value can't be null")
        self.value: _T = value

    def get(self) -> _T:
        return self.value

    def set(self, value: _T) -> Self:
        if value is None:
            raise ValueError("Holder value can't be null")
        self.value = value
        return self
