# NetSight — Master Execution Plan

This is the plan we follow. It is sequenced for **speed to a shippable MVP**, then
hardened toward the full automated, multi-camera vision.

Every phase has two tracks that run **in parallel**:

- **🧑 You (manual):** accounts, footage, hardware, labeling, real-world testing, parent recruiting.
- **🤖 Claude (software):** the code.

A phase is "done" when its **Exit criteria** are met. We do not gold-plate earlier
phases — we ship the thinnest thing that proves the next step is worth building.

---

## Guiding principles

1. **Offline before real-time.** Batch-process uploaded videos first. Real-time is a
   later optimization, not an MVP requirement. YouTube/film footage is offline by nature.
2. **Single camera before multi-camera.** One fixed wide-angle view gets us 80% of the
   value. Multi-camera is Phase 7.
3. **Human-in-the-loop before full auto.** The MVP ships with a fast review/correction
   UI. A human confirming the computer's box score is how we hit "good enough to show
   parents" on day one — and every correction becomes training data that drives the
   automation up. We reduce human effort each phase; we never block the product on
   reaching 100% automation.
4. **Stats first, fancy second.** A correct, trusted box score (kills, digs, aces,
   assists, errors, hitting %) is the product. Heatmaps, pose biomechanics, and
   highlight reels are upsells.
5. **Real volleyball scoring.** We mirror how coaches actually stat a match (see
   [`STATS_MODEL.md`](STATS_MODEL.md)) so the numbers are credible to anyone who knows
   the sport.

---

## Phase map at a glance

| Phase | Name | Outcome | Rough size |
| --- | --- | --- | --- |
| 0 | Planning | This plan, in the repo | ✅ now |
| 1 | CV spike | Players + ball detected & tracked on a real clip | small |
| 2 | Player identity & court | Each track ID'd to a jersey #; positions on a court model | medium |
| 3 | Stats engine + review UI | Verified box score per player from a full video | medium |
| 4 | Parent app (shippable MVP) | Parents log in, see player profiles, clips, rankings | medium |
| 5 | Accuracy hardening | Automation good enough to cut human review time sharply | ongoing |
| 6 | Productization | Billing, onboarding, multi-team, polish | medium |
| 7 | Multi-camera & real-time | Sync multiple cameras; live/near-live stats | large |

The **shippable-to-parents milestone is the end of Phase 4.** Everything after raises
quality and scale.

---

## Phase 0 — Planning ✅

**Outcome:** this document set, committed to the repo, so we have a shared map.

- 🤖 Claude: write `PLAN.md`, `ARCHITECTURE.md`, `STATS_MODEL.md`, `SETUP_CHECKLIST.md`, `DECISIONS.md`.
- 🧑 You: read `DECISIONS.md` and confirm/override the recommended defaults (hosting,
  budget, first test footage). See [`SETUP_CHECKLIST.md`](SETUP_CHECKLIST.md) §0.

**Exit criteria:** plan pushed; you've signed off on the Phase-1 footage and the stack defaults.

---

## Phase 1 — CV spike: detect & track on real footage

Prove the core perception works on actual volleyball video before building anything around it.

- 🤖 Claude:
  - Scaffold the `cv/` Python package and a `make spike VIDEO=<path>` entrypoint.
  - Pull frames from a local file (and a YouTube URL via `yt-dlp`).
  - Run **YOLO** (Ultralytics, pretrained COCO) to detect **people** and **the ball**.
  - Run **ByteTrack** to assign stable track IDs to each person across frames.
  - Render an annotated output video: boxes + track IDs + ball trail.
  - Emit a `tracks.json` (per-frame boxes, IDs) as the canonical intermediate format.
- 🧑 You:
  - Provide 2–3 game clips (1–3 min each) of the kind of footage we'll really get —
    ideally a fixed camera, whole court visible. One YouTube link + one phone clip is perfect.
  - Eyeball the annotated output and tell us where tracking breaks (occlusion, players
    swapping IDs, ball lost on fast spikes).

**Exit criteria:** on a real clip, players keep stable IDs through a rally most of the
time, and the ball is detected during serves/rallies often enough to be useful. We have
a documented sense of the failure modes.

---

## Phase 2 — Player identity & court geometry

Turn anonymous track IDs into *named players on a court*.

- 🤖 Claude:
  - **Jersey-number recognition:** crop each player track, OCR the number (PARSeq/EasyOCR),
    vote across frames so each track converges to a number despite motion blur.
  - **Re-ID embeddings:** appearance vectors so a player who's occluded and reappears
    re-links to the same identity (and, later, links across cameras).
  - **Court homography:** a one-time per-camera calibration (click the court corners /
    lines) mapping pixel positions → real court coordinates. Gives us "front row vs back
    row," zones 1–6, and which side a player is on.
  - **Roster mapping:** number → player name/position from a roster file you provide.
  - Persist an enriched `tracks.json` with `player_id`, court (x,y), and rotation/zone.
- 🧑 You:
  - Provide a **roster** per team (jersey #, name, position) — a simple form/spreadsheet.
  - Do the **court calibration** click-through for each camera angle (we build the tiny tool; you click 4–6 points).
  - Spot-check that numbers map to the right kids.

**Exit criteria:** for a test clip, most players are correctly named and placed on the
court model for most of the video, with a clear way to fix the ones that aren't.

---

## Phase 3 — Stats engine + human-in-the-loop review

Convert tracked, identified players + ball into a **volleyball box score**, with a fast
UI for a human to confirm/correct.

- 🤖 Claude:
  - **Event/touch detection:** use ball trajectory + player proximity + pose to segment
    rallies and detect touch events (serve, pass/reception, set, attack/spike, block, dig)
    and outcomes (kill, error, ace, continuation). This is the hard CV part — we start
    rules-based on trajectory/contacts and improve with the labeled data from review.
  - **Stat attribution:** map events → the stat model in [`STATS_MODEL.md`](STATS_MODEL.md)
    (kills, assists, digs, blocks, aces, reception 0–3, errors, hitting %).
  - **Review UI:** a timeline of detected rallies/touches synced to video. A human scrubs,
    confirms a touch, fixes the player or event type with one click, and approves the rally.
    Corrections are stored as ground-truth labels.
  - Produce a final, verified **match box score** + per-rally event log.
- 🧑 You:
  - Be the first **stat reviewer**: run a full game through the UI, correct it, and
    time how long it takes. Tell us where it's slow or wrong.
  - Validate the box score against reality (you watched the game / know the kids).

**Exit criteria:** a full game produces a box score you trust after a *reasonable*
review pass (target: review time well under live game length), and every correction is
captured as training data.

---

## Phase 4 — Parent app: the shippable MVP 🚢

Wrap the verified stats in a clean product parents can actually use.

- 🤖 Claude:
  - **Auth + teams** (Supabase): coach/admin accounts; parents invited to a team; each
    parent sees their player + team context (privacy-scoped — minors involved, so default to private).
  - **Player profile:** season + per-game stats, trend lines, strengths/weaknesses
    summary, and **clips** of that player's key plays (auto-cut from the event log).
  - **Team view & rankings:** leaderboard by contribution score (see STATS_MODEL), filterable.
  - **Upload flow:** coach uploads a video / pastes a YouTube link → job runs → review →
    publish to the team.
  - Deploy: frontend on Vercel, CV worker on a GPU host, Supabase for data/auth/storage.
- 🧑 You:
  - Recruit a **pilot team** (one team's parents) to test on.
  - Gather feedback: is the box score believable? Are clips the magic moment? What do
    parents actually open the app for?
  - Handle consent/permission for filming minors with that team.

**Exit criteria:** a real pilot team's parents log in and see trustworthy stats, clips,
and rankings for at least one real game. This is the first thing we can "deploy to parents."

---

## Phase 5 — Accuracy hardening (ongoing from here)

Drive human review time down and trust up using the data Phases 3–4 generate.

- 🤖 Claude:
  - Fine-tune detection/event models on our labeled volleyball data (vs. generic COCO).
  - Improve ball tracking through fast spikes (the hardest case) and contact detection.
  - Active learning: surface the rallies the model is least sure about for review first.
  - Track accuracy metrics per stat type so we know what's trustworthy to auto-publish.
- 🧑 You:
  - Keep reviewing games (each one improves the model); flag systematic errors.

**Exit criteria:** defined accuracy thresholds per stat where we let stats auto-publish
with light/no review.

---

## Phase 6 — Productization

Make it a business, not a demo.

- 🤖 Claude: billing/subscriptions, self-serve onboarding for new teams, season/tournament
  structures, exports (PDF box score, CSV), notifications ("new game stats are ready"),
  admin tooling, observability.
- 🧑 You: pricing, terms/privacy policy (minors data — important), marketing to clubs,
  support process.

**Exit criteria:** a new coach can sign up, pay, upload, and publish to their parents
without us in the loop.

---

## Phase 7 — Multi-camera & real-time

The full vision.

- 🤖 Claude:
  - **Multi-camera fusion:** time-sync feeds, fuse detections via the shared court
    homography + Re-ID so one player has one identity across all cameras; resolve
    occlusions one camera misses.
  - **Real-time path:** streaming inference for live/near-live stats during a match
    (scoreboard-style), reusing the offline pipeline's components.
  - Hardware guidance for gyms (camera placement, capture box).
- 🧑 You: camera hardware purchase/placement per [`SETUP_CHECKLIST.md`](SETUP_CHECKLIST.md) §7,
  gym access for a multi-cam test.

**Exit criteria:** a game captured by 2+ synced cameras yields a single fused, more
accurate stat set; a basic live stat view runs during a match.

---

## How we'll actually work, week to week

1. We work one phase at a time. I (Claude) open each phase by scaffolding the code and
   telling you exactly what manual input I need to proceed (footage, roster, a clicked
   calibration, an account).
2. You can almost always do your manual track **ahead** of me — e.g. gather Phase 1–3
   footage and rosters now (see the checklist) so I'm never blocked.
3. Each meaningful chunk gets committed and pushed to
   `claude/volleyball-vision-tracking-mvp-tqk8gk`. You can follow along in the repo.
4. We re-evaluate scope at each phase exit. The plan is a map, not a contract — if the
   CV spike reveals the ball is too hard to track on phone footage, we adapt (e.g.,
   require better camera placement) rather than plow ahead.

**Next action:** you confirm the Phase-0 decisions in [`DECISIONS.md`](DECISIONS.md) and
drop the first test clip + roster per [`SETUP_CHECKLIST.md`](SETUP_CHECKLIST.md); I start
Phase 1.
