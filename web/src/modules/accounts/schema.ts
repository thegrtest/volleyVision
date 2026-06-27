/**
 * Accounts module — users and their membership in teams (multi-tenant scoping).
 *
 * Auth provider (Supabase Auth / NextAuth) is wired in later; `users.id` is designed
 * to line up with an external auth subject id when that lands. For now it's a plain
 * table so the rest of the schema can reference it.
 */
import { pgTable, uuid, text, timestamp, pgEnum, unique } from "drizzle-orm/pg-core";
import { teams } from "../teams/schema";

/** A member's role within a team. Drives row-level access (parents see only their team). */
export const memberRole = pgEnum("member_role", ["owner", "coach", "parent"]);

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: text("email").notNull().unique(),
  name: text("name"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const teamMembers = pgTable(
  "team_members",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    teamId: uuid("team_id").notNull().references(() => teams.id, { onDelete: "cascade" }),
    userId: uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
    role: memberRole("role").notNull().default("parent"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [unique("team_members_team_user_unique").on(t.teamId, t.userId)],
);
