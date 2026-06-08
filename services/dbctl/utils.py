"""
manage and define helper functions to support
data import
data export
"""

import json
import zipfile
import csv
import logging
from pathlib import Path
from os import mkdir

from sqlalchemy import Table, inspect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.base import Base
from db.session import SessionLocal  # for session
from db.engine import engine  # engine
from config import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# get sorted tables
def get_sorted_tables() -> List[Table]:
    """return tables topologically, key=Foreign Key"""
    return Base.metadata.sorted_tables


def export_data(
    tables: list[str],
    fmt: str,
    version: str = "1.0",
    output_path: str = f"{config.PROJECT_ROOT}/data",
):
    """exports specified tables to a ZIP archive in topological order"""

    logger.info("[+] Starting data export")

    inspector = inspect(engine)

    # verify tables exist
    error = []
    __tables = inspector.get_table_names()

    for table in tables:
        if table not in __tables:
            error.append(table)
    else:
        if error:
            raise ValueError(f"Table not found {*error}")

    export_tables = [t for t in get_sorted_tables() if t.name in tables]

    metadata = {
        "fmt": fmt,
        "tables": [t.name for t in export_tables],
        "version": version,
    }

    Path(output_path).parent.mkdir(parent=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("metadata.json", json.dumps(metadata, indent=2))

        with SessionLocal() as session:
            for table in export_tables:
                filename = f"{table.name}.{fmt}"

                # using yield_per to stream large tables
                query = session.query(table).yield_per(1000)

                if fmt == "json":
                    data = [
                        {c.name: getattr(row, c.name) for c in table.columns}
                        for row in query
                    ]
                    archive.writestr(filename, json.dumps(data, default=str))
                else:
                    import io

                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow([c.name for c in table.columns])
                    for row in query:
                        writer.writerow([getattr(row, c.name) for c in table.columns])
                        archive.writestr(filename, output.getvalue())


def import_data(input_path: str, strategy: str, dry_run: bool = True):
    """import data from zip file"""
    if not Path(input_path).exists():
        raise FileNotFoundError("provided input path doens't exist")

    with zipfile.ZipFile(input_path, "r") as archive:
        meta = json.loads(archive.read("metadata.json"))

        fmt = meta["format"]
        version = meta["version"]
        tables_in_order = meta["tables"]

        with SessionLocal() as session:
            for table_name in tables_in_order:
                pass


__all__ = ["get_sorted_tables", "export_data", "import_data"]
