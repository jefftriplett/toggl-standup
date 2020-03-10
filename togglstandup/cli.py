"""
Installation:
  $ pipenv install click crayons humanfriendly maya togglwrapper

Configuration:
  $ export TOGGL_API_KEY="PASTE_YOUR_KEY_HERE"

Usage:
  $ python standup.py "yesterday"

"""

import click
import crayons
import maya
import os
import typer

from humanfriendly import format_timespan
from togglwrapper import Toggl

from .__version__ import __version__


cli = typer.Typer()


@cli.command()
def main(
    slang_date: str,
    show_time: bool = False,
    timezone: str = "US/Central",
    version: bool = False,
):
    """
    Standup tool to help with Toggl
    """
    toggl = Toggl(os.environ.get("TOGGL_API_KEY"))

    if version:
        click.echo(__version__)
        raise typer.Exit()

    now = maya.when(slang_date, timezone=timezone)
    now = now.datetime().replace(hour=6, minute=0, second=0, microsecond=0)
    now = maya.MayaDT.from_datetime(now)
    time_entries = toggl.TimeEntries.get(start_date=now.iso8601())

    last_start_slang = None
    for time_entry in time_entries:
        start = maya.when(time_entry["start"])
        start_slag = start.slang_date()
        if start_slag != last_start_slang:
            click.echo(crayons.green("## {0}".format(start.slang_date())))
        last_start_slang = start_slag

        project_id = time_entry.get("pid")
        if project_id:
            project = toggl.Projects.get(project_id)
            project_name = project["data"]["name"]
        else:
            project_name = ":question:"

        CMD = [
            "-",
            f"[{project_name}]",
            f"{time_entry['description']}",
            f"({format_timespan(time_entry['duration'])})",
            " :moneybag:" if time_entry["billable"] else "",
        ]

        if not show_time:
            del CMD[3]

        click.echo(" ".join(CMD))


if __name__ == "__main__":
    cli()
