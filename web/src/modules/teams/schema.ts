/**
 * Teams module — the top-level tenant. Every game, player, and stat hangs off a team.
 */
import { pgTable, uuid, text, timestamp } from "drizzle-orm/pg-core";

export const teams = pgTable("teams", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  /** URL-safe handle, e.g. "thunder-14u". */
  slug: text("slug").notNull().unique(),
  /** Age group / level label, e.g. "14U Club", "Varsity". Free text for now. */
  level: text("level"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});
