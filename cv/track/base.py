"""Tracker interface. ByteTrack (built on YOLOX) is the Phase 1 implementation.

A tracker consumes per-frame Detections and returns TrackedObjects carrying a stable
track_id across frames. People and the ball are tracked separately (very different motion
models), then merged per frame by the pipeline.
"""

from __future__ import annotations

from typing import Protocol

from cv.schemas.tracks import Detection, TrackedObject


class Tracker(Protocol):
    name: str

    def update(self, detections: list[Detection], frame_index: int) -> list[TrackedObject]:
        ...
