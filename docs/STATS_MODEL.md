# volleyVision — Stats & Ranking Model

For the product to be credible, the numbers must match how volleyball is **actually
statted by coaches**. This doc defines the events we detect, the stats we compute, and
the contribution score we rank on. The CV pipeline's job is to produce these events;
this doc is the source of truth for what they mean.

---

## 1. The touch events we detect

A rally is a sequence of **touches**. For each touch we capture: timestamp, player,
touch type, and outcome.

| Touch type | What it is |
| --- | --- |
| **Serve** | Player initiates the rally from behind the end line |
| **Reception (pass)** | First contact receiving a serve |
| **Dig** | Defensive contact off an opponent attack |
| **Set (assist touch)** | Second contact, delivering the ball to an attacker |
| **Attack (spike/hit)** | Aggressive attempt to score |
| **Block** | Contact at the net against an attack |
| **Free ball / cover** | Non-aggressive returns, tips, overpasses |

Each touch resolves to an **outcome**: `in_play` (continues), `point_won`, `point_lost`
(error), or a stat-specific result below.

---

## 2. The box score (standard volleyball stats)

These are the traditional categories. They are what coaches/recruiters recognize.

### Attacking
- **Kill (K):** attack that directly wins the point.
- **Attack Error (E):** attack that loses the point (out, into net, blocked for a point, etc.).
- **Total Attempts (TA):** all attacks.
- **Hitting Percentage:** `(K − E) / TA` — *the* headline attacking metric. (Range −1.0 to 1.0; .300+ is excellent.)

### Serving
- **Ace (SA):** serve that directly wins the point (untouched or unplayable).
- **Service Error (SE):** serve that loses the point (out/net/foot fault).
- **Serve attempts** and a 0–3 **serve effectiveness** rating (see §3).

### Passing / Serve-Receive
- **Reception attempts** and a 0–3 **pass rating** (see §3). Average pass rating
  (passer rating, ~0–3) is the headline serve-receive metric.
- **Reception Error (RE):** shanked/missed pass that loses the point.

### Defense
- **Dig (D):** successful defensive contact keeping an attacked ball in play.
- **Dig Error:** failed dig that loses the point.

### Setting
- **Assist (A):** set that leads directly to a kill (the volleyball equivalent of a basketball assist).
- **Ball-handling/Set Error (BHE):** mishandled set that loses the point.

### Blocking
- **Block Solo (BS):** single-player block that directly wins the point.
- **Block Assist (BA):** shared block that wins the point (credit split by convention; often 0.5 each).
- **Blocking Error (BE):** net/positioning fault giving up the point.

### Aggregate
- **Points (Pts):** the standard scoring formula coaches use:
  `Pts = Kills + Aces + Block Solos + 0.5 × Block Assists`.

> These are deliberately the **NCAA/USA-Volleyball-style** categories so a coach or
> recruiter reading our box score sees exactly what they expect.

---

## 3. The 0–3 rating scales (quality, not just counts)

Counts alone undervalue *quality*. Two scouting-standard 0–3 scales capture it:

**Pass / reception rating (per reception):**
- `3` Perfect — setter has all options.
- `2` Good — setter has most options.
- `1` Poor — setter limited / forced to chase.
- `0` Overpass or ace given up (or `RE` if it's an outright error).

**Serve rating (per serve):**
- `3` Ace / opponent out-of-system.
- `2` Opponent in trouble, no good attack.
- `1` Easy pass for opponent.
- `0` Service error.

We report the **average** of each per player. These are the metrics that show who
*quietly* makes the team better, beyond box-score counting stats.

---

## 4. Contribution score & ranking

This is the number we rank players on — designed to **credit real impact**, not just raw
counts, and to be fair across positions (a libero never gets kills; a setter rarely does).

### 4.1 Per-touch value
Every touch is assigned a value reflecting how much it helped/hurt the team's chance of
winning the point. Starting weights (tunable as we gather data):

| Event | Value |
| --- | --- |
| Kill | +1.0 |
| Ace | +1.0 |
| Block solo | +1.0 |
| Block assist | +0.5 |
| Assist (set → kill) | +0.5 |
| Dig (keeps attacked ball alive) | +0.3 |
| Reception rating 3 / 2 / 1 | +0.3 / +0.15 / +0.0 |
| Good set (in-system, no kill) | +0.1 |
| Attack error | −1.0 |
| Service error | −1.0 |
| Reception error / shank | −0.8 |
| Ball-handling / set error | −0.7 |
| Blocking error | −0.7 |

A player's **Raw Contribution** for a game = sum of their touch values.

### 4.2 Normalization (fair ranking)
Raw totals favor players who are on the court more and who play high-touch positions. So
rankings are computed on normalized variants, and the UI lets you switch between them:

- **Contribution per set/game** — rate, not volume.
- **Contribution per touch (efficiency)** — quality of involvement.
- **Position-adjusted percentile** — compare each player against others at the **same
  position** (setter vs setters, libero vs liberos), so a great libero ranks as a great
  libero rather than below every hitter.

The **default headline ranking** is *position-adjusted contribution per set* — it credits
real impact and is fair across roles.

### 4.3 Strengths & weaknesses
The same per-event data drives each player's profile:
- **Strengths:** the stat categories where they're in the top percentile (vs team and vs
  position).
- **Weaknesses:** their lowest percentile categories, framed constructively
  ("serve-receive is the biggest growth area").

---

## 5. Confidence & honesty

Every computed stat carries a **confidence** from the CV pipeline. Until Phase 5
accuracy thresholds are hit:
- Stats are **human-verified** before publishing (Phase 3 review UI).
- The app can show a subtle "verified" vs "auto" indicator so we never mislead a parent.

We would rather show fewer, trusted numbers than many shaky ones — credibility is the
whole product.

---

## 6. What we tune over time
The weights in §4.1 are a defensible starting point, not gospel. As we accumulate
labeled games we can fit weights to *actual point outcomes* (which touches most predict
winning points), turning the contribution score from a heuristic into a
data-driven impact metric — the genuinely novel part of the product.
