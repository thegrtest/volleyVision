# Production backend setup (Vercel + Postgres)

The public [GitHub Pages demo](./DEMO.md) is the **static frontend only**. This guide
stands up the **full app** — the Next.js server, its API routes, and a real Postgres
database — which is the production target described in [`ARCHITECTURE.md`](./ARCHITECTURE.md).

Nothing here is live yet; it's prepped so it's one signup away. Do the steps when you're
ready to create accounts.

---

## 1. Pick a Postgres provider

Either works; the schema is plain Postgres ([`web/drizzle/0000_init.sql`](../web/drizzle/0000_init.sql)).

| | **Neon** | **Supabase** |
| --- | --- | --- |
| Setup speed | Fastest (just a connection string) | Fast (also gives auth, storage, dashboard) |
| Best when | You only need Postgres now | You'll want auth/storage/file uploads later |
| Free tier | Yes | Yes |

The app's README recommends **Supabase**; **Neon** is the lightest if you only need the DB.

---

## 2. Wire it locally first (no deploy, works today)

```bash
cd web
cp .env.example .env.local            # then set DATABASE_URL in .env.local
npm run db:migrate                    # applies drizzle/*.sql to your database
npm run dev                           # http://localhost:3000
```

Confirm it worked:

```bash
curl http://localhost:3000/api/health      # expect:  "database": "ok"
```

`npm run db:studio` opens a browser UI to inspect the tables.

---

## 3. Deploy the full app to Vercel

1. **Import the repo** at https://vercel.com/new → select `thegrtest/volleyVision`.
2. **Set Root Directory = `web`.** ⚠️ Critical — the app lives in the `web/` subfolder, not
   the repo root. Vercel auto-detects Next.js once the root is correct.
3. **Add environment variables** (Project → Settings → Environment Variables):
   - `DATABASE_URL` — your provider's connection string
   - `NEXT_PUBLIC_SITE_URL` — e.g. `https://netsight.org` (optional)
4. **Deploy.** The lazy DB client means the build never connects, so the build succeeds
   even before migrations run.

The GitHub Pages workflow and the Vercel deploy are independent: Pages serves the static
marketing site; Vercel serves the full app. Point your real domain (netsight.org) at
Vercel when production is ready, and retire Pages then if you like.

---

## 4. Run migrations against the production database

Migrations are **not** run during the Vercel build (kept decoupled so a build never depends
on DB reachability). Run them explicitly, once per new migration:

```bash
# from web/, pointed at the production DB:
DATABASE_URL="<prod-connection-string>" npm run db:migrate
```

> **Connection gotcha:** run migrations over a **direct / session** connection, not a
> *transaction* pooler.
> - **Supabase:** use the **Session pooler** (port `5432`) or the direct connection for
>   `db:migrate`. The running app can use the transaction pooler (port `6543`) — the client
>   already sets `prepare: false` for pgbouncer compatibility ([`src/db/index.ts`](../web/src/db/index.ts)).
> - **Neon:** the pooled URL with `?sslmode=require` is fine.

The normal "add a feature" loop (edit a module's `schema.ts` → `npm run db:generate` →
review SQL → commit → `db:migrate`) is documented in [`web/README.md`](../web/README.md).

---

## 5. Make `/api/health` a live check again

For the static Pages export, the health route is pinned to a build-time snapshot:

```ts
// web/src/app/api/health/route.ts
export const dynamic = "force-static";
```

On a real server (Vercel) you want a live DB ping each request, so change it to:

```ts
export const dynamic = "force-dynamic";
```

⚠️ **Trade-off:** `force-dynamic` and the GitHub Pages static export are mutually exclusive —
`npm run build:static` will fail with `force-dynamic` because static export requires every
route handler to be static. So flip to `force-dynamic` only once Vercel is your primary host
and you've retired the Pages demo (or keep a static health snapshot and don't link to it).

---

## 6. Later: the CV worker

When the Python perception service ([`../cv/`](../cv/)) is hosted, set `CV_WORKER_URL` so the
app can hand off video-processing jobs. Not wired into the app code yet.
