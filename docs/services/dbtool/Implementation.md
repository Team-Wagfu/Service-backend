# Architecture and Design Decisions

## 1. Environment & Context
Connection contexts (`local` vs `render`) are handled by `src/dbtool/config.py`. The Click group injects the correct `Database URL` context into all subcommands, meaning no command is hardcoded to a specific DB.

## 2. Migration Strategy
We use Alembic programmatically. Rather than relying on `alembic upgrade head` in Bash, the CLI overrides the `sqlalchemy.url` within `migrations/env.py` at runtime.

## 3. Data Export/Import Protocol
**Topological Sorting:** We utilize `Base.metadata.sorted_tables` to guarantee parent tables (e.g., Users) are exported and imported *before* child tables (e.g., Projects) to prevent Foreign Key constraint violations.
**Format:** Archived ZIP containing a `metadata.json` for validation and schema tracking, alongside `.json` or `.csv` files per table. Chunked iteration via `.yield_per()` protects RAM.
**Upsert Logic:** PostgreSQL's native `on_conflict_do_update` is generated dynamically using the table's primary keys for seamless synchronization without duplicating rows.

## 4. Safety Constraints
Operations like `truncate`, `delete`, and `import` implement transactional scoping (`get_session` context manager). `--dry-run` forces an immediate `session.rollback()` prior to completion.