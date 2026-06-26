"""Render tracked objects onto frames: player boxes + ids, and a fading ball trail."""

from __future__ import annotations

from collections import deque

import cv2

from cv.schemas.tracks import TrackedObject, CLASS_BALL


def _color_for_id(track_id: int) -> tuple[int, int, int]:
    # Deterministic distinct-ish BGR color per track id.
    h = (track_id * 47) % 180
    hsv = (int(h), 200, 255)
    bgr = cv2.cvtColor(
        __import__("numpy").uint8([[hsv]]), cv2.COLOR_HSV2BGR
    )[0][0]
    return int(bgr[0]), int(bgr[1]), int(bgr[2])


class Annotator:
    def __init__(self, trail_len: int = 25):
        self._ball_trail: deque = deque(maxlen=trail_len)

    def draw(self, image, objects: list[TrackedObject]):
        for obj in objects:
            x1, y1, x2, y2 = (int(v) for v in obj.bbox)
            if obj.cls == CLASS_BALL:
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                self._ball_trail.append((cx, cy))
                cv2.circle(image, (cx, cy), max(4, (x2 - x1) // 2), (0, 255, 255), 2)
            else:
                color = _color_for_id(obj.track_id)
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                label = f"#{obj.track_id}"
                if obj.jersey_number is not None:
                    label += f" J{obj.jersey_number}"
                cv2.putText(image, label, (x1, max(12, y1 - 6)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Fading ball trail.
        pts = list(self._ball_trail)
        for i in range(1, len(pts)):
            cv2.line(image, pts[i - 1], pts[i], (0, 255, 255), 2)
        return image
