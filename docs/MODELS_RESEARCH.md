# NetSight — Off-the-Shelf Models & Datasets (verification)

**Question being verified:** can we skip training and use existing open-source volleyball
weights/datasets? **Verified 2026-06-26 by fetching each repo.**

**Bottom line:** Yes — availability is solved. Multiple downloadable volleyball-specific
**ball detectors** exist (90%+ precision reported), and a real labeled **action-recognition
dataset** exists too (better than first assumed). The actual work item is **licensing**:
the best ready-made weights are GPL/NonCommercial, fine for prototyping but not for the
shipped product — for production we plan to **train our own weights on a permissively
licensed dataset**.

---

## Ball detection — ✅ available off the shelf

| Source | What it gives | Reported quality | License | Use for us |
| --- | --- | --- | --- | --- |
| [jadidimohammad/volleyball-tracking](https://github.com/jadidimohammad/volleyball-tracking) | Downloadable YOLO v8–v26 weights trained on the **Volleyvision** dataset (~17k train / ~5k val); larger weights on MEGA | precision ~93–95%, recall ~87% | **GPL-3.0** | Prototype now; strong reference |
| [shukkkur/VolleyVision](https://github.com/shukkkur/VolleyVision) | YOLOv7-tiny weights + Roboflow AutoML model; 25k-image dataset | 74% mAP@50 (tiny) / 92% mAP@50 (AutoML) | **CC BY-NC-ND** | ⚠️ prototype/research **only** — non-commercial |
| [masouduut94/volleyball_analytics](https://github.com/masouduut94/volleyball_analytics) | Downloadable **ball segmentation** weights (`ball/weights/best.pt`) + dataset (Google Drive) | — | **GPL-2.0** | Prototype; dataset useful |

**Conclusion:** we can almost certainly **skip training a ball detector for the
prototype** and confirm whether default volleyball weights survive fast spikes on real
footage before investing anything.

## Action / event recognition — ✅ better than expected (a labeled dataset exists)

My earlier note said "no default exists." Verification softens that — there *is* prior art:

| Source | What it gives | License | Use for us |
| --- | --- | --- | --- |
| [mostafa-saad/deep-activity-rec](https://github.com/mostafa-saad/deep-activity-rec) (Ibrahim et al., CVPR 2016) | The standard **Volleyball Dataset**: 4,830 frames / 55 videos, player **bounding boxes** + **9 individual action labels** (spiking, blocking, setting, digging, jumping, standing, falling, waiting, moving) + 8 group-activity labels | **BSD 2-Clause** (code); dataset via Google Drive | ✅ permissive — directly trains our touch/action classifier |
| [masouduut94/volleyball_analytics](https://github.com/masouduut94/volleyball_analytics) | YOLOv8 **action detection** weights (service, reception, setting, blocking, spike) + **VideoMAE** game-state (service/play/no-play) + datasets | **GPL-2.0** | Prototype; validates the approach end-to-end |

**Conclusion:** per-player **action classification** has a real, permissively-licensed
training set (Ibrahim/BSD) and working example weights. We still build the layer that maps
*action + ball/point context → stat outcome* (kill/error/ace), but we are not starting
from zero.

---

## The real constraint: licensing (availability is not the problem)

| License | Repos | What it means for a commercial SaaS |
| --- | --- | --- |
| **CC BY-NC-ND** | shukkkur/VolleyVision | **Non-commercial** → prototype/feasibility only; cannot ship. |
| **GPL-2.0 / 3.0** | volleyball_analytics, jadidimohammad | Copyleft. Hosted SaaS doesn't "distribute," so it won't force us to open-source the backend — but mixing GPL *code* into our codebase is risky. Keep any GPL inference **isolated as a separate process/service**, or just use it to validate. |
| **BSD 2-Clause** | deep-activity-rec (Ibrahim) | Permissive — safe to use. (Dataset frames are from YouTube; fine for training, we don't redistribute footage.) |
| **Unverified** | Roboflow "Volleyvision" ball dataset (~22k imgs) | Page blocked automated fetch (403). **Action item:** check its license on the Roboflow page — if CC BY, we can **train our own commercially-clean ball weights** from it. |

### Recommended path
1. **Prototype (Phases 1–3):** use the ready GPL/Ibrahim weights to validate the whole
   pipeline fast and measure where default ball/action detection actually breaks.
2. **Production (Phase 4+):** retrain our **own** ball + action weights on
   permissively-licensed data (Ibrahim BSD dataset + a license-cleared Roboflow/Volleyvision
   set), keeping our model lineage clean for a commercial product. The Phase-3 review UI
   keeps adding our own labels on top.

This *confirms* the D11 "default-weights-first" decision and adds the nuance that the
weights we ship must be license-clean — an easy constraint to satisfy by training on
permissive datasets we've now located.

---

### Still to verify (small)
- Roboflow "Volleyvision" ball dataset license (blocked by 403 — check on-page).
- Whether any volleyball-specific weights handle the **fast-spike motion-blur** case well;
  only a test on real footage settles this (Phase 1).

Sources: the four repositories linked above.
