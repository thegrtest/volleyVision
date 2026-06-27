/**
 * drizzle-kit config — drives migration generation and pushes.
 *
 *   npm run db:generate   # diff schema -> new SQL migration in ./drizzle
 *   npm run db:migrate    # apply pending migrations
 *   npm run db:studio     # browse data
 *
 * Only used by the drizzle-kit CLI, never imported by the app build.
 */
import { config } from "dotenv";
import { defineConfig } from "drizzle-kit";

// Load .env.local first (Next convention), then .env as fallback.
config({ path: ".env.local" });
config({ path: ".env" });

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL ?? "postgres://localhost:5432/netsight",
  },
  // Keep migrations explicit and reviewable; no surprise auto-pushes.
  strict: true,
  verbose: true,
});
