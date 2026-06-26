# volleyVision

Computer-vision volleyball analytics. Upload a game video (YouTube link or file),
get **per-player stats, contribution scores, and rankings** — the kind of box score
a coach would tally by hand, generated automatically.

The product goal: parents and players see individual strengths, weaknesses, and
credit for real plays, ranked on real performance.

## Status

🟢 **Phase 0 — Planning.** This repo currently contains the execution plan only.
Code lands starting Phase 1.

## Read the plan first

| Doc | What it covers |
| --- | --- |
| [`docs/PLAN.md`](docs/PLAN.md) | The master phased roadmap, MVP → full deploy, with parallel **You** (manual) and **Claude** (software) tracks |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | The technical stack and how the CV pipeline, backend, and parent app fit together |
| [`docs/STATS_MODEL.md`](docs/STATS_MODEL.md) | How volleyball is actually scored, and our contribution/ranking formula |
| [`docs/SETUP_CHECKLIST.md`](docs/SETUP_CHECKLIST.md) | Your manual setup tasks — accounts, footage, hardware — to run in parallel with development |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Open decisions we need to lock, with recommended defaults |

## The one-paragraph version

Start **offline and single-camera**: a user uploads a game video, a Python CV
pipeline (YOLO detection → ByteTrack tracking → pose + jersey-number ID → court
homography → event attribution) produces a stat line per player, and a human
quickly verifies/corrects it in a review UI. A Next.js app shows parents clean
player profiles, clips, and rankings. We harden accuracy with the human-in-the-loop
data, automate more over time, then add real-time and multi-camera. This sequencing
gets something shippable to parents in weeks, not months, while building toward the
full automated vision.
