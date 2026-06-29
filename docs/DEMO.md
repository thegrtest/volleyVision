# Demo & GitHub Pages deploy

The visible product today is the **marketing landing page** ([`web/src/app/page.tsx`](../web/src/app/page.tsx)).
This guide covers running it for a demo and publishing it to GitHub Pages.

## What gets deployed (and what doesn't)

GitHub Pages serves **static files only** — there is no server. So the Pages site is the
**frontend landing page**, exported to plain HTML/CSS/JS. The API routes (`/api/health`)
and the database are **not** part of the Pages deploy; that backend is hosted separately
later (Vercel + managed Postgres — see [`ARCHITECTURE.md`](./ARCHITECTURE.md)).

This is intentional for a "test site now, productionize later" workflow.

## Two ways to run locally

```bash
cd web
npm install

# 1) Full app (server + API + DB) — the production-shaped dev server:
npm run dev                 # http://localhost:3000   (DB optional; /api/health is live)

# 2) The exact GitHub Pages artifact (static, no server):
npm run build:static        # emits ./out  (BUILD_STATIC=true under the hood)
npm run preview:static      # serves ./out at http://localhost:4000
# (any static server works, e.g.  python -m http.server 4000 --bind 127.0.0.1  from ./out)
```

Use **(1)** for backend/feature work, **(2)** to preview precisely what Pages will serve.

## Publish to GitHub Pages

A workflow is already staged at [`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml).
It builds `web/` as a static export and deploys it on every push to `main`.

This folder isn't a git repo yet. To go live (public, temporary test site):

```bash
# from the repo root: c:\Users\15017\Desktop\volleyVision-main
git init && git add -A && git commit -m "Initial commit: web app + cv scaffold"
gh repo create volleyVision --public --source=. --remote=origin --push
```

Then in the new repo: **Settings → Pages → Build and deployment → Source = "GitHub Actions".**
The first push triggers the workflow; the deploy job prints the live URL, which will be:

```
https://<your-username>.github.io/volleyVision/
```

> The workflow sets the asset base path to `/<repo-name>` automatically. If you later move
> to a custom domain (e.g. netsight.org) or a `<username>.github.io` root site, set
> `PAGES_BASE_PATH` to an empty string in the workflow.

When you're ready to take it private, GitHub Pages on private repos requires a paid plan —
otherwise unpublish Pages, or move the public demo to the eventual Vercel deployment.

## Notes / follow-ups

- **`/api/health` on the static site** is a build-time snapshot (it reads `force-static`
  in [`route.ts`](../web/src/app/api/health/route.ts) so the export can build). On a real
  server deploy, change that back to `force-dynamic` for a live DB ping. The static
  snapshot currently reports `database: "unconfigured"` since no DB is wired — harmless,
  but if you don't want the landing page's "Check system status" button showing that in a
  demo, repoint or hide the button for the static build.
- **Database** is intentionally skipped for this demo (nothing in the UI reads it yet).
  When a roster/stats screen needs data, wire `DATABASE_URL` (Neon/Supabase/local Postgres)
  and run `npm run db:migrate`. Full production backend setup (Vercel + Postgres) is in
  [`BACKEND.md`](./BACKEND.md).
- **The `cv/` pipeline** is not part of the web demo; it's a separate Python service.
