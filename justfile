set dotenv-load := false

@_default:
    just --list

@build:
    cog -r README.md

@fmt:
    just --fmt --unstable

@lint:
    black .

@update:
    poetry update
