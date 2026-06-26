"""Stub detector: synthetic moving boxes so the pipeline runs end-to-end without a model.

Lets us validate ingest → tracking → annotation → tracks.json IO independently of YOLOX.
Produces a few "players" drifting across the frame plus one fast "ball", so ByteTrack and
the annotator have realistic motion to chew on.
"""

from __future__ import annotations

import math

from cv.schemas.tracks import Detection, CLASS_PERSON, CLASS_BALL


class StubDetector:
    name = "stub"

    def __init__(self, n_players: int = 6):
        self.n_players = n_players
        self._t = 0

    def detect(self, image) -> list[Detection]:
        h, w = image.shape[:2]
        t = self._t
        self._t += 1
        dets: list[Detection] = []

        for i in range(self.n_players):
            cx = (w / (self.n_players + 1)) * (i + 1) + 20 * math.sin((t + i * 7) / 15)
            cy = h * 0.55 + 30 * math.sin((t + i * 11) / 23)
            bw, bh = w * 0.05, h * 0.18
            dets.append(Detection(
                CLASS_PERSON, 0.9,
                (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2),
            ))

        # A fast ball arcing across the court.
        bx = (t * 9) % w
        by = h * 0.35 + 120 * math.sin(t / 8)
        r = max(6, w * 0.012)
        dets.append(Detection(CLASS_BALL, 0.8, (bx - r, by - r, bx + r, by + r)))
        return dets
