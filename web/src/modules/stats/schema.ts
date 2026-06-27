/**
 * Stats module — the per-touch event log and the aggregated box score.
 *
 * This mirrors docs/STATS_MODEL.md exactly: `events` is the raw touch stream the CV
 * pipeline emits and humans verify; `player_game_stats` is the rolled-up box score the
 * app displays and ranks on. Aggregates are derived from events, so events are the
 * source of truth.
 */
import {
  pgTable, uuid, integer, real, boolean, timestamp, pgEnum,
} from "drizzle-orm/pg-core";
import { games } from "../games/schema";
import { players } from "../players/schema";

export const touchType = pgEnum("touch_type", [
  "serve",
  "reception",
  "set",
  "attack",
  "block",
  "dig",
  "free", // free ball / cover
]);

export const touchOutcome = pgEnum("touch_outcome", [
  "in_play",
  "kill",
  "attack_error",
  "ace",
  "service_error",
  "reception_error",
  "set_error",
  "block_solo",
  "block_assist",
  "block_error",
  "point_won",
  "point_lost",
]);

/** One touch in a rally. The atomic unit everything else is derived from. */
export const events = pgTable("events", {
  id: uuid("id").primaryKey().defaultRandom(),
  gameId: uuid("game_id").notNull().references(() => games.id, { onDelete: "cascade" }),
  playerId: uuid("player_id").references(() => players.id, { onDelete: "set null" }),
  setNumber: integer("set_number"),
  rallyNumber: integer("rally_number"),
  /** Seconds into the source video — lets the review UI jump straight to the touch. */
  tsSeconds: real("ts_seconds"),
  touchType: touchType("touch_type").notNull(),
  outcome: touchOutcome("outcome").notNull().default("in_play"),
  /** 0–3 pass/serve rating where applicable (see STATS_MODEL §3). */
  rating: integer("rating"),
  /** CV confidence 0..1; null once human-verified. */
  confidence: real("confidence"),
  verified: boolean("verified").notNull().default(false),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

/** Aggregated box score per player per game (derived from `events`). */
export const playerGameStats = pgTable("player_game_stats", {
  id: uuid("id").primaryKey().defaultRandom(),
  gameId: uuid("game_id").notNull().references(() => games.id, { onDelete: "cascade" }),
  playerId: uuid("player_id").notNull().references(() => players.id, { onDelete: "cascade" }),

  // Attacking
  kills: integer("kills").notNull().default(0),
  attackErrors: integer("attack_errors").notNull().default(0),
  attackAttempts: integer("attack_attempts").notNull().default(0),

  // Serving
  aces: integer("aces").notNull().default(0),
  serviceErrors: integer("service_errors").notNull().default(0),
  serveRatingAvg: real("serve_rating_avg"),

  // Serve-receive
  receptions: integer("receptions").notNull().default(0),
  receptionErrors: integer("reception_errors").notNull().default(0),
  passRatingAvg: real("pass_rating_avg"),

  // Defense / setting / blocking
  digs: integer("digs").notNull().default(0),
  assists: integer("assists").notNull().default(0),
  blockSolos: integer("block_solos").notNull().default(0),
  blockAssists: integer("block_assists").notNull().default(0),

  /** Raw contribution score per STATS_MODEL §4.1 (sum of weighted touch values). */
  contributionRaw: real("contribution_raw").notNull().default(0),

  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});
