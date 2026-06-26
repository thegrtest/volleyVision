# volleyVision — Open Decisions

A short list of decisions that shape the build. Each has a **recommended default** so we
can move fast — if the defaults are fine, just say "defaults are fine" and I'll proceed.
Override any you want.

| # | Decision | Recommended default | Why / trade-off |
| --- | --- | --- | --- |
| D1 | **Processing model** | Offline/batch (upload → process → review) | Fastest to ship; matches YouTube/film footage. Real-time deferred to Phase 7. |
| D2 | **First camera scope** | Single fixed camera | One wide view gets ~80% of value; multi-cam is a large later phase. |
| D3 | **MVP automation level** | Human-in-the-loop verified stats | Lets us show parents *trustworthy* numbers on day one while automation matures. |
| D4 | **Detection/tracking stack** | Ultralytics YOLO + ByteTrack | Best speed/accuracy/ergonomics; huge ecosystem; fine-tunable later. |
| D5 | **Pose** | MediaPipe to start | Your instinct; easy, runs anywhere. Path to RTMPose if multi-person robustness needs it. |
| D6 | **Data / Auth / Storage** | Supabase | Postgres + auth + storage + row-level security in one — fastest path to a real multi-tenant app, and RLS matters for minors' data. |
| D7 | **Parent app** | Next.js on Vercel | Trivial deploys, shareable preview links, mobile-friendly web (parents have phones). |
| D8 | **Backend** | FastAPI (Python) | Same language as CV; no serialization friction; async APIs. |
| D9 | **Privacy posture** | Strict / private-by-default, team-scoped, consent-gated | Non-negotiable for minors; shapes architecture from the start. No public leaderboards. |
| D10 | **Clips in MVP?** | Yes — auto-cut per-player highlights | Likely the emotional hook for parents; cheap given we already have the event timeline. |

## Decisions that need a *number/answer* from you (no good default I can pick)

| # | Question | Why I need it |
| --- | --- | --- |
| Q1 | **Monthly infra budget** while prototyping? (e.g. "<$100/mo to start") | Determines GPU instance tier and how aggressively we cache/batch. |
| Q2 | **First test footage** — what can you get me, and what's the *typical* footage you'll have long-term? | Decides how hard the CV must work (tripod vs phone-from-stands are very different). |
| Q3 | **Pilot team** — who's the first real team/parents we test on, and can you get filming consent? | This is the actual "ship to parents" target for Phase 4. |
| Q4 | **Geography/league** (e.g. USA Volleyball club, high school, NCAA-style) | Minor differences in stat conventions and what parents/recruiters expect. |

## Anything you want to change about the *plan itself*?
The phasing in [`PLAN.md`](PLAN.md) optimizes for "shippable to parents fastest" by going
offline + single-camera + human-verified first. If you'd rather, say, prioritize
real-time or multi-camera earlier, tell me and I'll re-sequence — but I'd recommend
against it for speed-to-MVP.
