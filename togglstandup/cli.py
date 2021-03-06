import crayons
import maya
import typer

from humanfriendly import format_timespan
from togglwrapper import Toggl

from .__version__ import __version__


cli = typer.Typer()


@cli.command()
def main(
    slang_date: str,
    api_key: str = typer.Option("", envvar="TOGGL_API_KEY", show_envvar=False),
    show_time: bool = False,
    timezone: str = "US/Central",
    version: bool = False,
):
    """
    Standup tool to help with Toggl
    """
    toggl = Toggl(api_key)

    if version:
        typer.echo(__version__)
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
            typer.echo(crayons.green("## {0}".format(start.slang_date())))
        last_start_slang = start_slag

        project_id = time_entry.get("pid")
        if project_id:
            project = toggl.Projects.get(project_id)
            project_name = project["data"]["name"]
        else:
            project_name = ":question:"

        cmd = [
            "-",
            f"[{project_name}]",
            f"{time_entry['description']}",
            f"({format_timespan(time_entry['duration'])})",
        ]

        if not show_time:
            del cmd[-1]

        typer.echo(" ".join(cmd))


if __name__ == "__main__":
    cli()
