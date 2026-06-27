/**
 * Health check: confirms the app is up and whether the database is reachable.
 * Used by deploy platforms and our own smoke tests. Runs at request time (Route
 * Handlers are uncached by default), so the DB ping is always live.
 */
import { sql } from "drizzle-orm";
import { getDb } from "@/db";

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
