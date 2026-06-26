"""Versioned data contract for the perception pipeline.

Stages communicate through these structures, serialized to JSON. Keeping the schema
explicit (and versioned) lets us swap or re-run any stage without breaking the others.
Phase 1 populates detections + track IDs; later phases fill player_id, court coords,
pose, etc. on the same TrackedObject without changing the contract shape.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional

SCHEMA_VERSION = "1.0"

# Class labels we care about in Phase 1. Maps to COCO ids when using a COCO-pretrained
# YOLOX (person=0, sports ball=32); a volleyball-fine-tuned model can override these.
CLASS_PERSON = "person"
CLASS_BALL = "ball"


@dataclass
class Detection:
    """One detected box in one frame (pre-tracking)."""
    cls: str                 # CLASS_PERSON | CLASS_BALL
    score: float             # detector confidence 0..1
    bbox: tuple[float, float, float, float]  # x1, y1, x2, y2 in pixels


@dataclass
class TrackedObject:
    """A detection that has been assigned a stable track id by the tracker.

    Fields beyond Phase 1 are optional and filled by later stages."""
    track_id: int
    cls: str
    score: float
    bbox: tuple[float, float, float, float]
    # ---- filled in Phase 2+ ----
    player_id: Optional[str] = None          # roster id once jersey # is resolved
    jersey_number: Optional[int] = None
    court_xy: Optional[tuple[float, float]] = None  # position on court plane (meters)
    zone: Optional[int] = None               # rotational zone 1..6


@dataclass
class FrameResult:
    frame_index: int
    timestamp_s: float
    objects: list[TrackedObject] = field(default_factory=list)


@dataclass
class VideoMeta:
    source: str              # file path or youtube url
    fps: float
    width: int
    height: int
    frame_count: int


@dataclass
class TracksDocument:
    """The full Phase 1 artifact written to tracks.json."""
    schema_version: str
    detector: str
    tracker: str
    video: VideoMeta
    frames: list[FrameResult] = field(default_factory=list)

    def to_json_dict(self) -> dict:
        return asdict(self)
