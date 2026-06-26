"""Detector interface. Any model (YOLOX, and later a fine-tuned one) implements this.

The whole point: the rest of the pipeline depends only on `Detector.detect()` returning
a list of `Detection`, so swapping models is a one-file change.
"""

from __future__ import annotations

from typing import Protocol

from cv.schemas.tracks import Detection


class Detector(Protocol):
    name: str

    def detect(self, image: "object") -> list[Detection]:
        """Run detection on one BGR frame; return person/ball Detections."""
        ...
