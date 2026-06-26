"""A small dependency-free IoU/centroid tracker.

This is a working baseline so the Phase 1 spike runs end-to-end today (no external
tracker install needed). ByteTrack replaces it for real footage via a sibling adapter
that implements the same `update()` — but this baseline is good enough to validate the
pipeline and to eyeball easy footage.

Greedy IoU matching with a short "lost" grace period so brief occlusions don't spawn new
ids. Per-class tracking (people vs ball never match each other).
"""

from __future__ import annotations

from dataclasses import dataclass

from cv.schemas.tracks import Detection, TrackedObject


def _iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    return inter / (area_a + area_b - inter)


@dataclass
class _Track:
    track_id: int
    cls: str
    bbox: tuple
    score: float
    missed: int = 0


class SimpleIouTracker:
    name = "simple_iou"

    def __init__(self, iou_threshold: float = 0.3, max_missed: int = 15):
        self.iou_threshold = iou_threshold
        self.max_missed = max_missed
        self._tracks: list[_Track] = []
        self._next_id = 1

    def update(self, detections: list[Detection], frame_index: int) -> list[TrackedObject]:
        unmatched = set(range(len(detections)))

        # Greedy match existing tracks to detections of the same class by best IoU.
        for tr in self._tracks:
            best_j, best_iou = -1, self.iou_threshold
            for j in unmatched:
                det = detections[j]
                if det.cls != tr.cls:
                    continue
                v = _iou(tr.bbox, det.bbox)
                if v >= best_iou:
                    best_iou, best_j = v, j
            if best_j >= 0:
                det = detections[best_j]
                tr.bbox, tr.score, tr.missed = det.bbox, det.score, 0
                unmatched.discard(best_j)
            else:
                tr.missed += 1

        # Spawn tracks for unmatched detections.
        for j in unmatched:
            det = detections[j]
            self._tracks.append(_Track(self._next_id, det.cls, det.bbox, det.score))
            self._next_id += 1

        # Retire stale tracks.
        self._tracks = [t for t in self._tracks if t.missed <= self.max_missed]

        # Report only currently-visible tracks (missed == 0).
        return [
            TrackedObject(track_id=t.track_id, cls=t.cls, score=t.score, bbox=t.bbox)
            for t in self._tracks if t.missed == 0
        ]
