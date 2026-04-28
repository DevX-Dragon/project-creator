# Project Creator

`prj-creator` is a Python CLI tool for scaffolding numbered project folders with optional templates for web, firmware, Python, docs, tests, and Git setup.

## What It Does

- Creates a new project folder using the next available number, for example `01.my-project`, `02.another-project`
- Lets you choose a setup style from the interactive wizard
- Generates common starter files such as `index.html`, `style.css`, `main.js`, `requirements.txt`, `.env.example`, and `blueprint.json`
- Can create a Python virtual environment
- Can initialize Git, set `main` as the branch, commit the project, and push to one or more remotes
- Can download template folders from a GitHub repository
- Bundled starter templates include `basic-web`, `npm-package`, and `python-pypi`

## Install

Install from Python packaging:

```bash
pip install prj-creator
```

If you want to work from source, install the dependencies listed in `src/pyproject.toml`:

```bash
pip install requests InquirerPy colorama rich GitPython
```

## Run

```bash
prj-creator
```

## CLI Options

The tool supports one command-line option for loading an external template source:

```bash
prj-creator --command source:https://github.com/user/repo
```

- `-c`, `--command`: load templates from an external GitHub repository in `source:https://...` form

## Interactive Modes

When you run the CLI normally, you will be asked to choose one of these modes:

- `Manual Setup`: choose features like web, API, firmware, docs, tests, and venv
- `Load Templates`: download a template from the default GitHub template repository
- `Empty Repository`: create a minimal project folder with a starter `README.md`

## Generated Structure

Typical output looks like this:

```text
01.my-project/
  web/
  api/
  firmware/
  docs/
  tests/
  venv/
  .env.example
  blueprint.json
  .gitignore
```

Not every folder is created every time. The final layout depends on the mode and toggles you select.

## Requirements

- Python
- `git`
- `pip`
- Internet access for cloud template downloads and remote Git pushes

## Notes

- Project folders are numbered by scanning the current directory for existing folders that start with a number and a dot.
- Git push only works if the remote is reachable and your credentials are already configured.
- The tool is designed for local project scaffolding, not for managing production deployments.

## Documentation

For the full software documentation, see [`docs/Documentation.md`](docs/Documentation.md).

## Contributing

If you want to add or improve templates, read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.
