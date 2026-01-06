from typing import Optional, Sequence, Tuple, Union


def validate(values: Sequence[Tuple[Optional[Union[str, int]], str]]) -> None:
    for value, name in values:
        if not value:
            raise ValueError(f"{name} must be set")
