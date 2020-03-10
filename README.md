# Stand Up for Toggl

This tool helps generate my daily Geekbot stand up report in an format which I may copy and paste into Slack.

## Usage

```shell
$ export TOGGL_API_KEY="PASTE_YOUR_KEY_HERE"

$ standup --help
Usage: standup [OPTIONS] SLANG_DATE

  Standup tool to help with Toggl

Options:
  --show-time / --no-show-time
  --timezone TEXT
  --version / --no-version
  --help                        Show this message and exit.
```

## To generate a report for yesterday

```shell
$ standup yesterday
```
