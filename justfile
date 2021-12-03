set dotenv-load := false

@_default:
    just --list

@build:
    cog -r README.md

@bump:
    bumpver update

@fmt:
    just --fmt --unstable

@lint:
    black .

@update:
    poetry add \
        humanfriendly@latest \
        maya@latest \
        rich@latest \
        togglwrapper@latest \
        typer@latest
