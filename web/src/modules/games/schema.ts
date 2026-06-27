/**
 * Games module — a match and the CV processing job that produces its stats.
 *
 * Lifecycle: uploaded → processing → review (human-in-the-loop) → published
 * (or failed). The `video_jobs` row tracks the cv/ pipeline run for a game.
 */
import { pgTable, uuid, text, timestamp, pgEnum } from "drizzle-orm/pg-core";
import { teams } from "../teams/schema";

export const gameStatus = pgEnum("game_status", [
  "uploaded",
  "processing",
  "review",
  "published",
  "failed",
]);

export const jobStatus = pgEnum("job_status", [
  "queued",
  "running",
  "succeeded",
  "failed",
]);

export const games = pgTable("games", {
  id: uuid("id").primaryKey().defaultRandom(),
  teamId: uuid("team_id").notNull().references(() => teams.id, { onDelete: "cascade" }),
  opponent: text("opponent"),
  playedAt: timestamp("played_at", { withTimezone: true }),
  /** Source video — a YouTube URL or an object-storage key for an uploaded file. */
  videoSource: text("video_source"),
  status: gameStatus("status").notNull().default("uploaded"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const videoJobs = pgTable("video_jobs", {
  id: uuid("id").primaryKey().defaultRandom(),
  gameId: uuid("game_id").notNull().references(() => games.id, { onDelete: "cascade" }),
  status: jobStatus("status").notNull().default("queued"),
  /** Where the cv/ artifacts (tracks.json, events.json, boxscore.json) landed. */
  artifactsUri: text("artifacts_uri"),
  error: text("error"),
  startedAt: timestamp("started_at", { withTimezone: true }),
  finishedAt: timestamp("finished_at", { withTimezone: true }),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});
