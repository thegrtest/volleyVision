# NetSight — Your Manual Setup Checklist

This is **your track**. Everything here is stuff a human has to do (accounts, footage,
hardware, real-world testing) and almost all of it can be done **ahead of the software**,
so I'm never blocked waiting on you. Items are grouped by the phase that needs them, but
feel free to race ahead.

Legend: ☐ to do · ⚡ unblocks me / do ASAP · 💳 may cost money · ⏳ can do anytime

---

## §0 — Before Phase 1 (do now)
- ☐ ⚡ **Confirm the stack decisions** in [`DECISIONS.md`](DECISIONS.md) (or just reply
  "defaults are fine"). I can't pick your budget/hosting for you.
- ☐ ⚡ **First test footage.** Give me **2–3 clips, 1–3 minutes each**, of real volleyball:
  - At least one from a **fixed camera with the whole court visible** (ideal input).
  - One **phone clip** like what a parent would actually capture (worst-case input).
  - A **YouTube link** to a similar game is also fine for the very first spike.
  - Drop files in `data/` (gitignored) or share links.
- ☐ ⏳ Tell me the **typical footage you expect to get** long-term (phone from the stands?
  a tripod cam? club livestream?). This decides how hard the CV has to work.

## §1 — Camera/footage quality (the single biggest accuracy lever)
- ☐ ⏳ For any footage *you* control, aim for: **camera elevated, behind/above one end
  line or at center side**, whole court + both end lines visible, steady (tripod), 1080p+,
  30fps+. The better this is, the better every downstream stat.
- ☐ ⏳ Avoid: heavy zoom/panning, backlight from gym windows, obstructed nets.

## §2 — Rosters & identity
- ☐ ⚡ For each team you want statted: a **roster** = jersey #, player name, primary
  position (S/OH/MB/OPP/L/DS). A spreadsheet or simple list is perfect; I'll give you a
  template. Numbers are how we ID players, so this is essential.
- ☐ ⏳ Note any **duplicate numbers across teams** and team jersey colors (helps ID).

## §3 — Becoming the first stat reviewer
- ☐ Plan to spend time in the **review UI** on the first full game once Phase 3 lands.
  You know the kids and the game, so you're the ideal first verifier. Budget ~the length
  of a game initially; it drops fast as automation improves.

## §4 — Pilot team (the "ship to parents" moment)
- ☐ ⏳ Line up **one friendly team** (ideally one you're connected to) whose parents will
  test the MVP and give honest feedback.
- ☐ ⚡ 💳 **Consent for minors.** Get parent/coach/club permission to film and process
  the kids' footage *before* we process it. This is legal/ethical table stakes since we
  handle minors' data — I'll help draft a simple consent blurb, but you own the
  relationships and sign-offs.
- ☐ ⏳ Collect what parents actually want to see (clips? rankings? recruiting stats?) —
  raw notes are gold.

## §5 — Accounts & services (I'll tell you exactly when each is needed)
Most are free to start. I'll wire the code; you create the account and paste me the keys
(into a secrets manager / `.env`, never committed).
- ☐ 💳 **GPU compute** for the CV worker (e.g. a cloud GPU instance, on-demand). Biggest
  cost lever; only runs while processing video. We'll pick the cheapest viable option.
- ☐ **Supabase** project (free tier fine to start) — DB/auth/storage.
- ☐ **Vercel** account — to host/deploy the parent app and share preview links.
- ☐ ⏳ A **domain name** when we're ready to show parents something branded (optional early).

## §6 — Decisions only you can make (see DECISIONS.md)
- ☐ Budget ceiling for monthly infra while prototyping.
- ☐ Privacy posture (I recommend strict/private-by-default for minors).
- ☐ Name/branding when we get to Phase 4.

## §7 — Multi-camera (Phase 7, much later — informational now)
- ☐ 💳 When we get here: **2+ cameras** with synchronized capture, mounted for
  complementary court coverage (e.g. each end line, or end + side). I'll spec exact
  models/placement based on what Phases 1–5 teach us — **don't buy anything yet.**
- ☐ Gym access for a multi-camera capture test.

---

### The fastest thing you can do right now
1. Reply on the [`DECISIONS.md`](DECISIONS.md) defaults.
2. Send me **one good clip + one phone clip + a roster** for the team in those clips.

That alone unblocks Phases 1–3. I'll start Phase 1 the moment a clip lands.
