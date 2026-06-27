# web/ — NetSight app & website

Next.js 16 (App Router, React 19, TypeScript, Tailwind v4) + Drizzle ORM over Postgres,
with migration-driven schema and a **modular** structure so features bolt on without
reshuffling the core.

## Quick start

```bash
cd web
npm install
cp .env.example .env.local        # set DATABASE_URL (Supabase/Neon/local Postgres)
npm run db:migrate                # apply migrations
npm run dev                       # http://localhost:3000
```

No database yet? The app still runs — `/api/health` reports `database: "unconfigured"`
instead of crashing.

## Database & migrations (the "as we go" workflow)

We use **Drizzle + drizzle-kit**. Schema lives in TypeScript; migrations are generated
SQL files you review and commit.

```bash
npm run db:generate   # diff schema -> new ./drizzle/NNNN_*.sql migration
npm run db:migrate    # apply pending migrations (used in CI/deploy too)
npm run db:push       # dev-only: push schema straight to a scratch DB, no migration file
npm run db:studio     # browse data in a UI
```

Typical change: edit a module's `schema.ts` → `npm run db:generate` → review the SQL →
commit both the schema and the migration. Migrations are immutable history; never edit a
committed one, always generate a new one.

## Modular expansion — how to add a feature

Each feature is a folder under `src/modules/<feature>/` that **owns its own tables**. The
registry in `src/db/schema.ts` re-exports them so drizzle-kit sees one surface.

To add, say, a `notifications` feature:

1. `src/modules/notifications/schema.ts` — define its tables.
2. Add `export * from "../modules/notifications/schema";` to `src/db/schema.ts`.
3. `npm run db:generate` → review → commit.

That's the entire contract. Modules don't reach into each other's internals; they
reference by foreign key (e.g. `players.teamId → teams.id`).

## Layout

```
web/
├── drizzle/                  # generated SQL migrations (committed)
├── drizzle.config.ts         # drizzle-kit config
├── src/
│   ├── app/                  # Next.js App Router (routes, layouts, API)
│   │   ├── page.tsx          # marketing landing
│   │   ├── layout.tsx        # root layout + metadata
│   │   └── api/health/route.ts   # health + DB ping
│   ├── db/
│   │   ├── index.ts          # lazy Drizzle client (getDb())
│   │   ├── schema.ts         # MODULE REGISTRY — re-exports every module's tables
│   │   └── migrate.ts        # standalone migration runner for deploy
│   └── modules/              # FEATURE MODULES, each owns its schema
│       ├── accounts/         # users + team membership (roles)
│       ├── teams/            # tenants
│       ├── players/          # roster (jersey #, position)
│       ├── games/            # matches + CV processing jobs
│       └── stats/            # touch events + aggregated box score
└── .env.example
```

The `db/index.ts` client is **lazy** — importing it never connects, so `next build`
needs no database. Connections open at request time inside server routes.

## Domain model (current)

Mirrors [`../docs/STATS_MODEL.md`](../docs/STATS_MODEL.md) and the `cv/` pipeline output:

- **teams** → **players** (roster, jersey # = identity anchor)
- **games** → **video_jobs** (a cv/ pipeline run; lifecycle uploaded→processing→review→published)
- **events** (per-touch log the pipeline emits & humans verify) → **player_game_stats**
  (rolled-up box score the app ranks on)
- **users** + **team_members** (role-scoped access; parents see only their team)

## Hosting

Built to deploy on **Vercel** (frontend/API) against a managed Postgres (**Supabase**
recommended — see `../docs/ARCHITECTURE.md`). `npm run db:migrate` runs as a deploy step.
The heavy CV worker is a separate Python service (`../cv/`); the app talks to it over
`CV_WORKER_URL` and reads its artifacts — keeping web and GPU concerns independently
scalable.
