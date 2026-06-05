from dataclasses import asdict, dataclass


@dataclass
class CompareResponse:
    success: bool
    match_percent: float
    similarity: float
    is_match: bool
    threshold: float
    distance: float
    message: str = "So khớp thành công"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ErrorResponse:
    success: bool
    message: str

    def to_dict(self) -> dict:
        return asdict(self)
