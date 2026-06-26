"""Phase 1 spike CLI.

Examples:
    python -m cv.spike --video data/clip.mp4 --out out
    python -m cv.spike --youtube "https://youtu.be/XXXX" --out out --seconds 120
    python -m cv.spike --video data/clip.mp4 --detector yolox \
        --weights weights/yolox.pth --out out
"""

from __future__ import annotations

import argparse
import sys

from cv.ingest.video import VideoSource
from cv.pipeline import run_pipeline


def build_detector(args):
    if args.detector == "stub":
        from cv.detect.stub_detector import StubDetector
        return StubDetector()
    if args.detector == "yolox":
        if not args.weights:
            sys.exit("--weights is required for --detector yolox")
        from cv.detect.yolox_detector import YoloxDetector
        return YoloxDetector(
            weights=args.weights, exp_file=args.exp,
            conf_threshold=args.conf, device=args.device,
        )
    sys.exit(f"unknown detector: {args.detector}")


def build_tracker(args):
    if args.tracker == "simple":
        from cv.track.simple_tracker import SimpleIouTracker
        return SimpleIouTracker()
    # Placeholder for the ByteTrack adapter (cv/track/bytetrack_tracker.py).
    sys.exit(f"unknown tracker: {args.tracker}")


def main():
    p = argparse.ArgumentParser(description="volleyVision Phase 1 detect+track spike")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--video", help="path to a local video file")
    src.add_argument("--youtube", help="YouTube URL")
    p.add_argument("--out", default="out", help="output directory")
    p.add_argument("--seconds", type=float, default=None, help="cap processing length")
    p.add_argument("--stride", type=int, default=1, help="process every Nth frame")

    p.add_argument("--detector", default="stub", choices=["stub", "yolox"])
    p.add_argument("--weights", help="YOLOX weights (.pth) for --detector yolox")
    p.add_argument("--exp", help="YOLOX exp file")
    p.add_argument("--conf", type=float, default=0.25)
    p.add_argument("--device", default="cuda")

    p.add_argument("--tracker", default="simple", choices=["simple", "bytetrack"])
    args = p.parse_args()

    detector = build_detector(args)
    tracker = build_tracker(args)

    with VideoSource(
        path=args.video, youtube=args.youtube,
        max_seconds=args.seconds, stride=args.stride,
    ) as source:
        run_pipeline(source, detector, tracker, args.out)


if __name__ == "__main__":
    main()
