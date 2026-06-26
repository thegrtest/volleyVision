"""Phase 1 orchestration: ingest → detect → track → annotate → write tracks.json.

Keeps the stages decoupled: this file knows the order, not the internals. Swapping the
detector (stub → YOLOX) or tracker (simple → ByteTrack) is a constructor change only.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict

import cv2
from tqdm import tqdm

from cv.annotate import Annotator
from cv.ingest.video import VideoSource
from cv.schemas.tracks import (
    SCHEMA_VERSION, FrameResult, TracksDocument,
)


def run_pipeline(source: VideoSource, detector, tracker, out_dir: str) -> TracksDocument:
    os.makedirs(out_dir, exist_ok=True)
    meta = source.meta
    annotator = Annotator()

    writer = None
    annotated_path = os.path.join(out_dir, "annotated.mp4")

    doc = TracksDocument(
        schema_version=SCHEMA_VERSION,
        detector=getattr(detector, "name", "unknown"),
        tracker=getattr(tracker, "name", "unknown"),
        video=meta,
        frames=[],
    )

    total = meta.frame_count if meta.frame_count > 0 else None
    for frame in tqdm(source.frames(), total=total, desc="processing", unit="f"):
        detections = detector.detect(frame.image)
        tracked = tracker.update(detections, frame.index)

        doc.frames.append(FrameResult(
            frame_index=frame.index,
            timestamp_s=round(frame.timestamp_s, 4),
            objects=tracked,
        ))

        annotated = annotator.draw(frame.image, tracked)
        if writer is None:
            h, w = annotated.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(annotated_path, fourcc, meta.fps, (w, h))
        writer.write(annotated)

    if writer is not None:
        writer.release()

    tracks_path = os.path.join(out_dir, "tracks.json")
    with open(tracks_path, "w") as f:
        json.dump(doc.to_json_dict(), f)

    print(f"\nWrote {tracks_path} ({len(doc.frames)} frames)")
    print(f"Wrote {annotated_path}")
    return doc
