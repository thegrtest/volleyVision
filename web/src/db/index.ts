/**
 * Database client (Drizzle + postgres.js).
 *
 * Lazily initialized so importing this module never connects at build time — the
 * client is only created on first `getDb()` call, which happens inside server routes
 * at request time. Works against any Postgres (Supabase, Neon, local docker).
 */
import { drizzle, type PostgresJsDatabase } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

export type Database = PostgresJsDatabase<typeof schema>;

let _db: Database | null = null;

export function getDb(): Database {
  if (_db) return _db;
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error(
      "DATABASE_URL is not set. Copy .env.example to .env.local and point it at a Postgres instance.",
    );
  }
  // prepare:false keeps it compatible with connection poolers (e.g. Supabase pgbouncer).
  const client = postgres(url, { prepare: false });
  _db = drizzle(client, { schema });
  return _db;
}

export { schema };
