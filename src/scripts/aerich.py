import asyncio
import sys
from pathlib import Path
from aerich.cli import cli


async def run_aerich_command(args: list[str]):
    try:
        await cli.main(args)
    except SystemExit:
        pass

def init():
    """Initialize Aerich for a new project."""
    asyncio.run(run_aerich_command(["init", "-t", "src.core.database.TORTOISE_ORM"]))


def makemigrations():
    asyncio.run(cli.main(["migrate"]))


def migrate():
    asyncio.run(cli.main(["upgrade"]))


def mount():
    """Initialize the database (create schema tables)."""
    asyncio.run(run_aerich_command(["init-db"]))