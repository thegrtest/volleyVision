"""YOLOX detector adapter.

This is the single integration point for the existing in-house YOLOX project. Fill in the
three TODOs (import, load weights, map outputs) and the detector plugs into the whole
pipeline. Everything else in cv/ is model-agnostic.

Keeping this thin and isolated means we don't fork YOLOX — we call into it.
"""

from __future__ import annotations

from typing import Optional

from cv.schemas.tracks import Detection, CLASS_PERSON, CLASS_BALL

# COCO class ids for a COCO-pretrained YOLOX. A volleyball-fine-tuned model can remap these.
COCO_PERSON_ID = 0
COCO_SPORTS_BALL_ID = 32

_COCO_TO_OURS = {COCO_PERSON_ID: CLASS_PERSON, COCO_SPORTS_BALL_ID: CLASS_BALL}


class YoloxDetector:
    name = "yolox"

    def __init__(
        self,
        weights: str,
        exp_file: Optional[str] = None,
        conf_threshold: float = 0.25,
        nms_threshold: float = 0.45,
        device: str = "cuda",
        class_map: Optional[dict[int, str]] = None,
    ):
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold
        self.device = device
        self.class_map = class_map or _COCO_TO_OURS

        # TODO(yolox-1): import the existing YOLOX project.
        #   from yolox.exp import get_exp
        #   from yolox.utils import postprocess
        #   self._exp = get_exp(exp_file)
        #
        # TODO(yolox-2): build the model and load weights onto self.device.
        #   self._model = self._exp.get_model().to(device).eval()
        #   ckpt = torch.load(weights, map_location=device)
        #   self._model.load_state_dict(ckpt["model"])
        raise NotImplementedError(
            "Wire YoloxDetector to the in-house YOLOX project (see TODOs). "
            "Until then run the spike with --detector stub."
        )

    def detect(self, image) -> list[Detection]:
        # TODO(yolox-3): preprocess `image` (BGR ndarray), run the model, postprocess
        # with conf/nms thresholds, then map each (cls_id, score, x1,y1,x2,y2) to a
        # Detection, keeping only classes present in self.class_map.
        #
        #   raw = self._infer(image)
        #   dets = []
        #   for cls_id, score, (x1, y1, x2, y2) in raw:
        #       if cls_id in self.class_map and score >= self.conf_threshold:
        #           dets.append(Detection(self.class_map[cls_id], float(score),
        #                                 (x1, y1, x2, y2)))
        #   return dets
        raise NotImplementedError
