/**
 * Health check: confirms the app is up and whether the database is reachable.
 * Used by deploy platforms and our own smoke tests. Runs at request time (Route
 * Handlers are uncached by default), so the DB ping is always live.
 */
import { sql } from "drizzle-orm";
import { getDb } from "@/db";

// `output: export` (the GitHub Pages static build) requires every route handler to
// declare a static rendering mode, and Next only accepts a literal here. A static
// host has no server or DB, so a build-time snapshot is the correct semantics there.
// NOTE: when the backend is deployed to a real server (Vercel), change this back to
// "force-dynamic" so the DB ping runs live on every request again.
export const dynamic = "force-static";

export async function GET() {
  let database: "ok" | "unconfigured" | "error" = "ok";
  let detail: string | undefined;

  try {
    await getDb().execute(sql`select 1`);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    database = message.includes("DATABASE_URL") ? "unconfigured" : "error";
    detail = message;
  }

  return Response.json({
    status: database === "ok" ? "ok" : "degraded",
    service: "netsight-web",
    database,
    ...(detail ? { detail } : {}),
    time: new Date().toISOString(),
  });
}
