# Project Creator CLI

`prj-creator` is a Python CLI for scaffolding numbered project folders with optional web, firmware, API, docs, tests, and Git setup.

## Install

```bash
pip install prj-creator
```

If you are developing from source, install the project dependencies from `src/pyproject.toml`:

```bash
pip install requests InquirerPy colorama rich GitPython
```

## Run

```bash
prj-creator
```

## What It Creates

- Numbered project folders like `01.my-project`
- `web/` starter files
- `api/main.py`
- `firmware/<project-name>.ino`
- `docs/` and `tests/` folders
- `.env.example`
- `blueprint.json`
- `.gitignore`
- Optional `venv/`
- Bundled templates: `basic-web`, `npm-package`, `python-pypi`

## Cloud Templates

The built-in cloud template mode downloads folders from:

```text
https://api.github.com/repos/DevX-Dragon/project-creator/contents/templates
```

## Git Support

The tool can initialize a Git repository, set `main` as the branch, commit the generated files, and push to one or more remotes.

## License

Distributed under the [MIT License](../LICENSE)

###### Made by @DevX-Dragon, a developer from Sri Lanka.
