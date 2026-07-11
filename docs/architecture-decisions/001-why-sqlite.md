# 001 - Why SQLite

## Status
Accepted

## Context
The pipeline needs to persist two kinds of data: raw, unprocessed records
coming straight from extractors, and cleaned/aggregated data used for
ROI analysis. We needed a storage solution that's simple to set up, works
locally without extra infrastructure, and fits a project of this scale
(a personal data pipeline, not a multi-user production service).

Options considered:
- **PostgreSQL / MySQL**: more powerful, support concurrent writes well,
  but require running a separate database server. Overkill for a project
  that runs locally and doesn't need to scale to multiple users.
- **SQLAlchemy (ORM)**: would abstract away raw SQL, but adds a layer of
  complexity and "magic" that isn't necessary here, and doesn't match
  the SQL fundamentals this project was meant to reinforce.
- **SQLite (raw sqlite3 module)**: built into Python, zero setup, stores
  everything in a single file, and is more than capable of handling the
  data volume this pipeline deals with.

## Decision
Use Python's built-in `sqlite3` module with raw SQL queries, not an ORM.

Two separate database files are used:
- `raw_staging.db` - stores raw extractor output as-is (JSON blobs), before
  any cleaning happens. Keeping raw data around makes it possible to
  re-run transformation logic later without hitting external APIs again.
- `pipeline.db` - stores the cleaned, structured data: Skills, SkillMetrics
  (demand counts per source), and ROIScores.

## Consequences
- No extra setup required to run the project locally - just clone and go.
- Full control over the SQL being run, which keeps the storage layer
  transparent and easy to debug.
- Doesn't scale to concurrent multi-user access, but that's not a
  requirement for this project.
- If the project ever needed to move to a "real" database (Postgres, etc.),
  the raw SQL would need to be rewritten - there's no ORM abstraction
  cushioning that migration. Acceptable tradeoff given the project's scope.