# volleyVision — Technical Architecture

This describes the stack and how the pieces fit. It's chosen for **fast shipping** and
for being the right long-term foundation (real-time + multi-camera) without a rewrite.

## North star: one pipeline, two modes

The same perception components run **offline (batch)** for the MVP and **streaming
(real-time)** later. We build offline first because it's simpler and matches YouTube/film
footage. Real-time (Phase 7) reuses the same stages on a frame stream.

```
                    ┌────────────────────────────────────────────────────┐
  Video / YouTube → │  CV PIPELINE (Python)                               │
                    │                                                     │
                    │  1. Ingest    yt-dlp / ffmpeg → frames              │
                    │  2. Detect    YOLO (Ultralytics): people + ball     │
                    │  3. Track     ByteTrack: stable per-person IDs      │
                    │  4. Identify  jersey-number OCR + Re-ID embeddings  │
                    │  5. Localize  court homography → court (x,y), zones  │
                    │  6. Pose      MediaPipe/RTMPose (for contacts/biomech)│
                    │  7. Events    rallies + touches (serve/set/spike/…)  │
                    │  8. Stats     events → box score (STATS_MODEL.md)    │
                    └───────────────┬─────────────────────────────────────┘
                                    │ tracks.json, events.json, boxscore.json
                                    ▼
        ┌──────────────────────────────────────────────┐
        │  BACKEND (FastAPI)                            │
        │  job queue, storage, REST/realtime API        │
        └───────────────┬───────────────┬──────────────┘
                        │               │
          ┌─────────────▼───┐   ┌───────▼─────────────────┐
          │ REVIEW UI       │   │ PARENT APP (Next.js)    │
          │ verify/correct  │   │ profiles, clips, ranks  │
          │ stats (HITL)    │   │ deployed on Vercel      │
          └─────────────────┘   └─────────────────────────┘

   Data/Auth/Storage: Supabase (Postgres + Auth + Object Storage)
```

## Why these choices

### CV pipeline — Python
- **YOLOX** for player + ball detection (reusing existing in-house YOLOX projects/weights).
  Pretrained to start; fine-tuned on our labeled volleyball data in Phase 5. ByteTrack was
  built on YOLOX by the same team, so the detector→tracker handoff is native.
- **ByteTrack** (or BoT-SORT) for multi-object tracking — strong at keeping IDs through the
  brief occlusions volleyball is full of, and pairs natively with YOLOX.
- **Jersey number OCR**: scene-text recognizers (PARSeq / EasyOCR) on player crops, with
  multi-frame voting. Jersey number is our practical identity anchor.
- **Re-ID embeddings** (e.g. OSNet): appearance vectors to re-link players after occlusion
  and, later, across cameras.
- **Court homography** (OpenCV): map image → court plane from a one-time corner/line
  calibration. Unlocks zones, rotation, front/back row — needed for correct stat rules.
- **Pose**: MediaPipe Pose to start (the user's instinct — easy, runs anywhere), with a path
  to RTMPose for multi-person robustness. Pose helps detect *contacts* (who touched the ball)
  and later powers biomechanics/technique feedback.
- **Events**: start **rules-based** on ball trajectory + player proximity + pose contacts to
  segment rallies and classify touches; upgrade to a learned temporal model as labeled data
  accumulates. This is the hardest part and where human-in-the-loop earns its keep.

> **Note on "MediaPipe alone":** MediaPipe is excellent for pose, but it does not by itself do
> multi-player tracking across a court, jersey-number ID, ball tracking, or event attribution.
> So MediaPipe is *one stage* (pose) in a larger pipeline rather than the whole system. The plan
> reflects that.

### Intermediate data contract
Stages communicate via versioned JSON artifacts so we can swap/upgrade any stage and
re-run downstream without redoing everything:
- `tracks.json` — per frame: detections, track IDs, player_id, court coords, pose.
- `events.json` — rallies and touch events with timestamps, player, type, outcome, confidence.
- `boxscore.json` — aggregated per-player/per-team stats (the published artifact).

These also make the **review UI** straightforward: it edits `events.json`, recomputes
`boxscore.json`, and stores diffs as labels.

### Backend — FastAPI
Same language as the CV code (no serialization friction). Responsibilities: accept uploads,
enqueue processing jobs (Redis + RQ/Celery), serve REST + realtime APIs to the apps, manage
publish/review state. CV workers run on a **GPU host** (the only piece needing a GPU).

### Data / Auth / Storage — Supabase
Postgres + Auth + object storage + row-level security in one managed service = the fastest
path to a real multi-tenant, parent-facing app. RLS matters because **we're handling minors'
data** and must scope each parent strictly to their team. Swappable later if we outgrow it.

### Parent app — Next.js on Vercel
React app for player profiles, trends, clips, and rankings. Vercel = trivial deploys and
preview URLs to share with the pilot team. Mobile-friendly web first (parents have phones);
native wrappers later only if needed.

### Clips
The event log gives us exact timestamps, so we auto-cut per-player highlight clips with ffmpeg.
Clips are likely the emotional hook for parents — prioritized in the MVP.

## Deployment topology (MVP)

| Component | Host | Notes |
| --- | --- | --- |
| Parent app (Next.js) | Vercel | preview + prod |
| Backend API (FastAPI) | small cloud VM / container | cheap, always-on |
| CV worker | GPU instance (on-demand) | spins up per job; biggest cost lever |
| DB/Auth/Storage | Supabase | managed |
| Queue/cache | Redis (managed) | jobs |

Offline batch means the **GPU only runs while processing a video**, so cost scales with
usage, not uptime — important for an early-stage budget.

## Repo layout (target)

```
volleyVision/
├── docs/                 # this plan
├── cv/                   # Python CV pipeline (the heart)
│   ├── ingest/ detect/ track/ identify/ court/ pose/ events/ stats/
│   ├── pipeline.py       # orchestrates stages → JSON artifacts
│   └── schemas/          # versioned JSON contracts
├── backend/              # FastAPI app + workers
├── web/                  # Next.js parent app + review UI
├── infra/                # deploy config, IaC, env templates
└── data/                 # local test footage & labels (gitignored)
```

## Privacy & safety (non-negotiable, called out early)
- Footage and stats involve **minors**. Default everything to **private**, team-scoped.
- Explicit consent flow before a team's footage is processed/shared (Phase 4/6).
- No public leaderboards by default; rankings live inside a team's authenticated space.
- This shapes architecture now (RLS, scoped storage), not as a bolt-on later.
