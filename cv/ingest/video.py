"""Video ingest: yield frames from a local file or a YouTube URL.

YouTube URLs are resolved with yt-dlp to a direct stream that OpenCV can read, so we
never have to download the whole file first. Frames come out as (index, timestamp_s,
BGR ndarray), which is exactly what the detector/annotator consume.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Iterator, Optional

import cv2

from cv.schemas.tracks import VideoMeta


@dataclass
class Frame:
    index: int
    timestamp_s: float
    image: "cv2.typing.MatLike"


def resolve_youtube_url(url: str) -> str:
    """Return a direct media URL OpenCV/ffmpeg can open, via yt-dlp.

    Prefers a progressive mp4 <=720p for fast, reliable decoding during the spike.
    """
    cmd = [
        "yt-dlp", "-g",
        "-f", "best[ext=mp4][height<=720]/best[height<=720]/best",
        url,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    # yt-dlp -g may print video and audio URLs on separate lines; take the first.
    direct = out.stdout.strip().splitlines()[0]
    return direct


class VideoSource:
    """Iterable frame source with metadata, for either a file or a YouTube URL."""

    def __init__(
        self,
        path: Optional[str] = None,
        youtube: Optional[str] = None,
        max_seconds: Optional[float] = None,
        stride: int = 1,
    ):
        if not path and not youtube:
            raise ValueError("Provide either path= or youtube=")
        self.source_label = youtube or path
        self._open_target = resolve_youtube_url(youtube) if youtube else path
        self.max_seconds = max_seconds
        self.stride = max(1, stride)

        self.cap = cv2.VideoCapture(self._open_target)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open video: {self.source_label}")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def meta(self) -> VideoMeta:
        return VideoMeta(
            source=self.source_label,
            fps=self.fps,
            width=self.width,
            height=self.height,
            frame_count=self.frame_count,
        )

    def frames(self) -> Iterator[Frame]:
        idx = 0
        while True:
            ok, image = self.cap.read()
            if not ok:
                break
            ts = idx / self.fps
            if self.max_seconds is not None and ts > self.max_seconds:
                break
            if idx % self.stride == 0:
                yield Frame(index=idx, timestamp_s=ts, image=image)
            idx += 1

    def close(self) -> None:
        self.cap.release()

    def __enter__(self) -> "VideoSource":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
