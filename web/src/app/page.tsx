import Link from "next/link";

const features = [
  {
    title: "Per-player stats",
    body: "Kills, digs, aces, assists, hitting % — the box score a coach tallies by hand, generated from game video.",
  },
  {
    title: "Contribution score",
    body: "A position-fair impact rating so a great libero ranks as a great libero — not below every hitter.",
  },
  {
    title: "Highlight clips",
    body: "Every player's key plays auto-cut from the footage parents already want to watch.",
  },
  {
    title: "Strengths & growth",
    body: "Each player sees what they're best at and the one area to work on next — framed for development.",
  },
];

const steps = [
  { n: 1, title: "Add footage", body: "Upload a game video or paste a YouTube link." },
  { n: 2, title: "We process it", body: "NetSight detects players, the ball, and every touch." },
  { n: 3, title: "Verify & publish", body: "A quick review confirms the box score, then it's live for the team." },
];

export default function Home() {
  return (
    <main className="flex-1">
      {/* Hero */}
      <section className="mx-auto max-w-5xl px-6 pt-24 pb-16 text-center">
        <p className="inline-block rounded-full border border-black/10 px-3 py-1 text-xs font-medium tracking-wide text-foreground/60 dark:border-white/15">
          netsight.org · early access
        </p>
        <h1 className="mt-6 text-4xl font-bold tracking-tight sm:text-6xl">
          See every player&apos;s game.
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-foreground/70">
          NetSight turns volleyball video into per-player stats, a fair contribution
          score, and highlight clips — so players see their strengths, get credit for
          real plays, and are ranked on real performance.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Link
            href="/api/health"
            className="rounded-full bg-foreground px-6 py-3 text-sm font-semibold text-background transition hover:opacity-90"
          >
            Check system status
          </Link>
          <a
            href="https://github.com/thegrtest/volleyVision"
            className="rounded-full border border-black/10 px-6 py-3 text-sm font-semibold transition hover:bg-black/5 dark:border-white/15 dark:hover:bg-white/5"
          >
            View the build
          </a>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-5xl px-6 py-12">
        <div className="grid gap-6 sm:grid-cols-2">
          {features.map((f) => (
            <div
              key={f.title}
              className="rounded-2xl border border-black/10 p-6 dark:border-white/10"
            >
              <h3 className="text-lg font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-foreground/70">{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mx-auto max-w-5xl px-6 py-12">
        <h2 className="text-center text-2xl font-bold tracking-tight">How it works</h2>
        <div className="mt-10 grid gap-8 sm:grid-cols-3">
          {steps.map((s) => (
            <div key={s.n} className="text-center">
              <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-foreground text-sm font-bold text-background">
                {s.n}
              </div>
              <h3 className="mt-4 font-semibold">{s.title}</h3>
              <p className="mt-1 text-sm text-foreground/70">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="mx-auto max-w-5xl px-6 py-16 text-center text-sm text-foreground/50">
        © {new Date().getFullYear()} NetSight · Built for players, parents, and coaches.
      </footer>
    </main>
  );
}
