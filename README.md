# Stand Up for Toggl

This tool helps generate my daily Geekbot stand up report in an format which I may copy and paste into Slack.

## Usage
<!-- [[[cog
import cog
from typer.testing import CliRunner
from togglstandup.cli import cli
runner = CliRunner()
result = runner.invoke(cli, ["--help"])
help = result.output.replace("Usage: main", "Usage: standup")
cog.outl("```shell")
cog.outl("$ export TOGGL_API_KEY='PASTE_YOUR_KEY_HERE'\n")
cog.outl("$ standup --help\n")
cog.outl("{}```".format(help))
]]] -->
```shell
$ export TOGGL_API_KEY='PASTE_YOUR_KEY_HERE'

$ standup --help

Usage: standup [OPTIONS] SLANG_DATE

  Standup tool to help with Toggl

Arguments:
  SLANG_DATE  [required]

Options:
  --api-key TEXT                  [default: ]
  --show-duration / --no-show-duration
                                  [default: False]
  --show-time / --no-show-time    [default: False]
  --timezone TEXT                 [default: US/Central]
  --version
  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to copy
                                  it or customize the installation.

  --help                          Show this message and exit.
```
<!-- [[[end]]] -->

## To generate a report for yesterday

```shell
$ standup yesterday
```
