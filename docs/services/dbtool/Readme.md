# <PROJECT_PACKAGE_NAME> (dbtool)

A Click-based CLI for PostgreSQL management via SQLAlchemy and Alembic.

## Installation
1. Ensure PostgreSQL client tools (`pg_dump`, `pg_restore`) are installed.
2. `poetry install`
3. Copy `.env.example` to `.env` and fill in placeholders.

## Quick Usage Examples
Switch between databases using the `--env` flag (defaults to local).

```bash
# Initialize DB and apply migrations
dbtool --env local init

# Create a new migration based on model updates
dbtool migrate --auto -m "Added roles"

# Export models to JSON archive
dbtool --env render export --models users,projects --format json --output ./exports/dump.zip

# Import with Upsert strategy (Dry-run to test)
dbtool --env local import --input ./exports/dump.zip --strategy upsert --dry-run

# Backup Render DB
dbtool --env render backup --output ./backups/prod.dump

# View table stats
dbtool stats