import maya
import typer

from humanfriendly import format_timespan
from rich import print
from togglwrapper import Toggl
from typing import Optional

from .__version__ import __version__


cli = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"toggl-standup version: {__version__}")
        raise typer.Exit()


@cli.command()
def main(
    slang_date: str,
    api_key: str = typer.Option("", envvar="TOGGL_API_KEY", show_envvar=False),
    show_duration: bool = False,
    show_time: bool = False,
    timezone: str = "US/Central",
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback
    ),
):
    """
    Standup tool to help with Toggl
    """
    toggl = Toggl(api_key)

    if version:
        print(__version__)
        raise typer.Exit()

    now = maya.when(slang_date, timezone=timezone)
    now = now.datetime().replace(hour=6, minute=0, second=0, microsecond=0)
    now = maya.MayaDT.from_datetime(now)
    time_entries = toggl.TimeEntries.get(start_date=now.iso8601())

    last_start_slang = None
    for time_entry in time_entries:
        if time_entry["start"]:
            start = maya.when(time_entry["start"])
            start_slag = start.slang_date()
        else:
            start = None
            start_slag = None

        if time_entry["stop"]:
            stop = maya.when(time_entry["stop"])
            stop_slag = stop.slang_time()
        else:
            stop = None
            stop_slag = None

        if start_slag != last_start_slang:
            print(f"[bold green]## {start.slang_date()}[/bold green]")

        last_start_slang = start_slag

        project_id = time_entry.get("pid")
        if project_id:
            project = toggl.Projects.get(project_id)
            project_name = project["data"]["name"]
        else:
            project_name = ":question:"

        cmd = ["-"]

        if show_time:
            cmd += [
                f"{start.hour:02}:{start.minute:02}",
                "-",
                f"{stop.hour:02}:{stop.minute:02}",
                "-",
            ]

        cmd += [
            f"[{project_name}]",
            f"{time_entry.get('description', '')}",
            f"({format_timespan(time_entry['duration'])})",
        ]

        if not show_duration:
            del cmd[-1]

        print(" ".join(cmd))


if __name__ == "__main__":
    typer.run(cli)
