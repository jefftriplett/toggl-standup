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

from click_default_group import DefaultGroup
from humanfriendly import format_timespan
from togglwrapper import Toggl

from .__version__ import __version__


@click.group(cls=DefaultGroup, default='main', default_if_no_args=True)
@click.version_option(prog_name='toggl-standup', version=__version__)
def cli():
    """
    Standup tool to help with Toggl
    """


@cli.command()
@click.option('--show-time/--no-show-time', default=False)
@click.argument('slang_date')
def main(slang_date, show_time):
    toggl = Toggl(os.environ.get('TOGGL_API_KEY'))

    now = maya.when(slang_date, timezone='US/Central')
    now = now.datetime().replace(hour=6, minute=0, second=0, microsecond=0)
    now = maya.MayaDT.from_datetime(now)
    time_entries = toggl.TimeEntries.get(start_date=now.iso8601())

    last_start_slang = None
    for time_entry in time_entries:
        start = maya.when(time_entry['start'])
        start_slag = start.slang_date()
        if start_slag != last_start_slang:
            click.echo(
                crayons.green(
                    '## {0}'.format(start.slang_date())
                )
            )
        last_start_slang = start_slag

        project_id = time_entry.get('pid')
        if project_id:
            project = toggl.Projects.get(project_id)
            project_name = project['data']['name']
        else:
            project_name = ':question:'

        if show_time:
            click.echo(
                '- [{project_name}] {description} ({duration}){billable}'.format(
                    project_name=project_name,
                    description=time_entry['description'],
                    duration=format_timespan(time_entry['duration']),
                    billable=' :moneybag:' if time_entry['billable'] else ''
                )
            )
        else:
            click.echo(
                '- [{project_name}] {description}{billable}'.format(
                    project_name=project_name,
                    description=time_entry['description'],
                    billable=' :moneybag:' if time_entry['billable'] else ''
                )
            )


if __name__ == '__main__':
    main()
