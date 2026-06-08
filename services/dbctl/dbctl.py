import click
import subprocess
import os
import logging

from pathlib import Path
from config import config
from db.session import SessionLocal
from db.engine import engine
from services.cmdline.utils import import_data, export_data, get_sorted_tables

from sqlalchemy import text, inspect

logger=logging.getLogger(__name__)

@click.group()
@click.option('--env', type=click.Choice['local','prod'], default='local', help='Set target DB')
@click.option('--log-level', default='INFO', help='Set Logging level')
@click.pass_context
def cli(ctx, env, log_level):
    try:
        logger.setLevel(log_level)
        ctx.obj = "" # the shared object
        