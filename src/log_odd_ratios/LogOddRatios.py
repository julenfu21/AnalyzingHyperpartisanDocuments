from dataclasses import dataclass, field

from src.constant_values.enums import TokenType


@dataclass
class LogOddRatios:
    values: dict[str, float] = field(default_factory=dict)
    type: TokenType = field(default=TokenType)
