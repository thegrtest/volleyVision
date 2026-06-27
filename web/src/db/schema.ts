/**
 * Root schema — re-exports every module's tables so drizzle-kit sees one surface
 * to diff and generate migrations from. To add a feature, create
 * `src/modules/<feature>/schema.ts` and re-export it here. That's the whole "modular
 * expansion" contract: modules own their tables, this file is the registry.
 */
export * from "../modules/accounts/schema";
export * from "../modules/teams/schema";
export * from "../modules/players/schema";
export * from "../modules/games/schema";
export * from "../modules/stats/schema";
