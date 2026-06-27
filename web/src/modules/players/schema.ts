/**
 * Players module — roster entries. Jersey number is the identity anchor the CV
 * pipeline maps to (see docs/STATS_MODEL.md and the cv/ identity stage).
 */
import { pgTable, uuid, text, integer, timestamp, pgEnum, unique } from "drizzle-orm/pg-core";
import { teams } from "../teams/schema";

/** Standard volleyball positions. */
export const playerPosition = pgEnum("player_position", [
  "S", // setter
  "OH", // outside hitter
  "MB", // middle blocker
  "OPP", // opposite / right side
  "L", // libero
  "DS", // defensive specialist
  "UTIL", // utility / unspecified
]);

export const players = pgTable(
  "players",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    teamId: uuid("team_id").notNull().references(() => teams.id, { onDelete: "cascade" }),
    name: text("name").notNull(),
    jerseyNumber: integer("jersey_number"),
    position: playerPosition("position").notNull().default("UTIL"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  // A jersey number is unique within a team (nulls allowed for unassigned).
  (t) => [unique("players_team_jersey_unique").on(t.teamId, t.jerseyNumber)],
);
