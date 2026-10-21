"""Optional chart samples. They never substitute for an evaluated scalar value."""
from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, AwareDatetime, StrictBool, model_serializer, model_validator
from typing import Annotated, Literal, Union

Number = Union[StrictBool, Annotated[int, Field(strict=True, ge=-9007199254740991, le=9007199254740991)], Annotated[float, Field(strict=True, allow_inf_nan=False, ge=-9007199254740991, le=9007199254740991)]]

class Point(BaseModel):
    model_config = ConfigDict(extra='forbid')
    at: AwareDatetime
    value: Number | None

class Event(BaseModel):
    model_config = ConfigDict(extra='forbid')
    at: AwareDatetime
    label: str = Field(min_length=1, max_length=160)
    kind: Literal['fault_start', 'fault_end', 'detected', 'acknowledged', 'mitigated', 'recovered', 'note'] = 'note'

class Series(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: str = Field(min_length=1, max_length=2000)
    expected_interval_seconds: int | None = Field(default=None, ge=1, le=604800, strict=True)
    points: list[Point] = Field(min_length=1, max_length=20000)
    events: list[Event] = Field(default_factory=list, max_length=100)

class SeriesEvidenceMixin(BaseModel):
    # Omit the absent extension to preserve canonical legacy records and hashes.
    series: Series | None = None

    @model_serializer(mode='wrap')
    def serialize_series(self, handler):
        data = handler(self)
        if data.get('series') is None:
            data.pop('series', None)
        return data

    @model_validator(mode='after')
    def check_series(self):
        if self.series is None:
            return self
        previous = None
        for point in self.series.points:
            if not self.window_start <= point.at <= self.window_end:
                raise ValueError('Chart samples must be within the evidence measurement window')
            if previous is not None and point.at <= previous:
                raise ValueError('Chart sample timestamps must be strictly increasing')
            if point.value is not None and isinstance(point.value, bool) != isinstance(self.value, bool):
                raise ValueError('Chart samples and scalar summary must have the same numeric/boolean type')
            previous = point.at
        if any(not self.window_start <= e.at <= self.window_end for e in self.series.events):
            raise ValueError('Chart events must be within the evidence measurement window')
        return self
