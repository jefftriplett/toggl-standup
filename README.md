# Stand Up for Toggl

This tool helps generate my daily Geekbot stand up report in an format which I may copy and paste into Slack.

## Usage

```shell
$ export TOGGL_API_KEY="PASTE_YOUR_KEY_HERE"
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
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

## To generate a report for yesterday

```shell
$ standup yesterday
```
