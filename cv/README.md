# cv/ — the NetSight perception pipeline

Phase 1 scope: **ingest a video (file or YouTube) → detect people + ball → track them
with stable IDs → render an annotated video → emit `tracks.json`.**

Later phases add identity (jersey #/Re-ID), court homography, pose, events, and stats —
each as a stage that reads the previous stage's JSON artifact.

## Design: pluggable stages, JSON contracts

Stages are decoupled by versioned JSON artifacts (`cv/schemas/`) so any stage can be
swapped or re-run without redoing the others. The detector and tracker are behind small
interfaces (`cv/detect/base.py`, `cv/track/base.py`) so **your existing YOLOX project
drops in by implementing one `detect()` method** — no rewrite.

## Run the Phase 1 spike

```bash
cd cv
pip install -r requirements.txt          # add YOLOX/ByteTrack per their repos (see below)

# From a local file:
python -m cv.spike --video ../data/clip.mp4 --out ../out

# From a YouTube link:
python -m cv.spike --youtube "https://youtu.be/XXXX" --out ../out --seconds 120
```

Outputs to `--out`: `annotated.mp4` (boxes + track IDs + ball trail) and `tracks.json`.

## Wiring in your YOLOX project

`cv/detect/yolox_detector.py` is a thin adapter with a single integration point. Point it
at your YOLOX repo + weights and map its output to our `Detection` dataclass. Until that's
wired, `--detector stub` runs the whole pipeline end-to-end on synthetic detections so we
can validate ingest/tracking/annotation/IO independently of the model.

> **Status:** scaffold committed. It needs `pip install` deps + your YOLOX weights to run
> for real; the structure, data contract, ingest, annotation, and orchestration are in
> place so we only have to slot the model in.
