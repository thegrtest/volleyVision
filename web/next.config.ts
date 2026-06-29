import type { NextConfig } from "next";

/**
 * Two build modes share this one config:
 *
 *  - Default (`next dev` / `next build` / `next start`): the full app — App Router,
 *    API routes, and DB — runs on a Node server. This is the production target
 *    (Vercel + managed Postgres).
 *
 *  - Static export (`BUILD_STATIC=true next build`): emits a self-contained `out/`
 *    folder of plain HTML/CSS/JS for static hosts like **GitHub Pages**. There is no
 *    server, so API routes/DB are not part of this artifact — it's the marketing
 *    frontend only. Used for the public demo before the backend is hosted.
 *
 * `PAGES_BASE_PATH` is set by the deploy workflow to the repo subpath (e.g.
 * "/volleyVision") so assets resolve under `username.github.io/<repo>/`. Left unset
 * for local preview, the export serves cleanly from the root.
 */
const isStaticExport = process.env.BUILD_STATIC === "true";
const basePath = process.env.PAGES_BASE_PATH || "";

const nextConfig: NextConfig = isStaticExport
  ? {
      output: "export",
      // Pages serves files, not a server, so image optimization must be off and
      // routes are emitted as directories (`/path/index.html`).
      images: { unoptimized: true },
      trailingSlash: true,
      ...(basePath ? { basePath, assetPrefix: basePath } : {}),
      // Expose the base path to client code that needs to build links/asset URLs.
      env: { NEXT_PUBLIC_BASE_PATH: basePath },
    }
  : {};

export default nextConfig;
