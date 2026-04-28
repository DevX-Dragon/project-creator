# Project Creator Software Documentation

## 1. Purpose

Project Creator is a Python-based CLI scaffolding tool. Its job is to take a project name, pick the next numeric folder prefix, and generate a ready-to-use workspace with optional web, firmware, Python, documentation, testing, and Git setup.

The main entry point is [`src/prj_creator/main.py`](../src/prj_creator/main.py), which exposes the console script `prj-creator`.

## 2. Package Overview

### Package metadata

The package is defined in [`src/pyproject.toml`](../src/pyproject.toml).

- Package name: `prj-creator`
- Current version: `2.1.3`
- Console script: `prj-creator = prj_creator.main:run_wizard`

### Runtime dependencies

The project declares these Python dependencies:

- `requests`
- `InquirerPy`
- `colorama`
- `rich`
- `GitPython`

These are used for GitHub API access, interactive prompts, terminal styling, and Git repository management.

## 3. Installation

### From PyPI

```bash
pip install prj-creator
```

### From source

If you are running the repo locally, install the declared dependencies:

```bash
pip install requests InquirerPy colorama rich GitPython
```

Then run the package entry point through your environment:

```bash
prj-creator
```

## 4. System Requirements

The CLI checks for these tools at startup:

- `git`
- `python`
- `pip`

If any of them are missing from `PATH`, the program exits before continuing.

The cloud template mode also requires internet access because it talks to the GitHub API.

## 5. Startup Flow

When `prj-creator` starts, it performs this sequence:

1. Checks for required system tools.
2. Fixes terminal behavior on Windows so Unicode and color output work properly.
3. Clears the screen.
4. Prints the project banner.
5. Prompts for the project name.
6. Prompts for the mode:
   - Manual Setup
   - Load Templates
   - Empty Repository
7. Creates the next numbered project folder.
8. Applies the selected setup flow.
9. Prompts for optional Git remote URL(s).
10. Initializes Git and pushes when remotes were provided.
11. Opens the created project folder at the end on supported platforms.

## 6. Project Numbering

Project names are turned into folders using this pattern:

```text
NN.project-name
```

The number is determined by scanning the current working directory for existing folders that begin with a numeric prefix followed by a dot.

Example:

- Existing folders: `01.alpha`, `02.beta`
- New folder: `03.my-project`

This means the numbering is based on the directory you launch the tool from, not a global counter.

## 7. Modes

### 7.1 Manual Setup

Manual Setup is the most feature-rich mode. It lets you toggle these options:

- `web`
- `venv`
- `api`
- `firm`
- `docs`
- `tests`

#### What each toggle creates

- `web`
  - Creates a `web/` folder
  - Creates empty starter files: `index.html`, `style.css`, `main.js`

- `venv`
  - Creates a Python virtual environment in `venv/`
  - If `api` is also selected, installs `fastapi` and `uvicorn` into that environment

- `api`
  - Creates an `api/` folder
  - Writes a basic `api/main.py` containing a minimal FastAPI app

- `firm`
  - Creates a `firmware/` folder
  - Writes an Arduino sketch named after the project, for example `my-project.ino`

- `docs`
  - Creates a `docs/` folder in the generated project

- `tests`
  - Creates a `tests/` folder in the generated project

#### Extra files generated in Manual Setup

Manual Setup also creates:

- `.env.example`
- `blueprint.json`
- `.gitignore`

The generated `.env.example` is a placeholder file with variables such as `DEBUG` and `SECRET_KEY`. If `api` is selected, it also includes API-related placeholders.

The `blueprint.json` file stores a small metadata object with:

- project name
- selected features
- version

### 7.2 Load Templates

Load Templates downloads a template folder from the repository configured in the code:

- Default user: `DevX-Dragon`
- Default repository: `project-creator`
- API path: `https://api.github.com/repos/DevX-Dragon/project-creator/contents/templates`
- Bundled template directories:
  - `basic-web`
  - `npm-package`
  - `python-pypi`

The tool:

1. Queries the GitHub contents API for available template directories
2. Prompts you to choose a template
3. Downloads the selected template folder recursively into the new project directory

### 7.3 Empty Repository

Empty Repository creates the project folder and writes a minimal `README.md` with the project title. This is the lightest possible scaffold.

## 8. Git Behavior

After the selected mode completes, the tool asks for optional Git remote URL(s).

If one or more URLs are entered, the tool will:

1. Run `git init`
2. Add the first remote as `origin`
3. Rename the branch to `main`
4. Stage the generated files
5. Create an initial commit
6. Push to `main`

If multiple remote URLs are provided, they should be comma-separated. The first one becomes `origin`, and additional ones are named `remote-1`, `remote-2`, and so on.

### Git command intent

The current implementation uses GitPython for repository setup and pushes. In practical terms, it is automating the same flow a user would perform manually:

- initialize repository
- ensure `main`
- create the first commit
- push to the remote repository

### Important Git note

The tool does not manage your credentials. Authentication still depends on your local Git setup.

## 9. External Source Mode

You can also launch the tool with:

```bash
prj-creator --command source:https://github.com/user/repo
```

This path is handled by `handle_external_source()` in [`src/prj_creator/main.py`](../src/prj_creator/main.py).

### Behavior

1. The string after `source:` is parsed as a GitHub repository URL.
2. The tool fetches `templates/` from that repository.
3. It shows the available template directories.
4. It asks for a project name.
5. It downloads the selected template into a folder named after the project.

This mode is useful when you want to pull templates from a repository other than the built-in default.

## 10. File Outputs

### Root project files

Depending on the selected mode and toggles, the generated root folder may contain:

- `.gitignore`
- `.env.example`
- `blueprint.json`
- `README.md`
- `requirements.txt`
- `venv/`

### Web output

When `web` is enabled:

- `web/index.html`
- `web/style.css`
- `web/main.js`

### API output

When `api` is enabled:

- `api/main.py`

### Firmware output

When `firm` is enabled:

- `firmware/<project-name>.ino`

### Docs and tests

When selected:

- `docs/`
- `tests/`

## 11. Error Handling

The CLI is designed to keep going where possible, but there are a few important failure points:

- Missing required system tools cause an immediate exit.
- Git push can fail if the remote is empty, unavailable, or authentication is not configured.
- Cloud template downloads can fail if the GitHub API is unavailable or the repository layout does not match expectations.
- External source mode depends on the repository exposing a `templates/` directory.

Most runtime errors are caught and printed to the console instead of crashing with a full traceback.

## 12. Implementation Notes

The key functions in [`src/prj_creator/main.py`](../src/prj_creator/main.py) are:

- `check_system_health()`
  - Verifies `git`, `python`, and `pip` are available

- `fix_terminal()`
  - Applies Windows console fixes for UTF-8 and ANSI color output

- `get_next_num()`
  - Scans the current directory and computes the next folder number

- `download_remote_folder()`
  - Recursively downloads a GitHub repository folder

- `handle_git_logic()`
  - Writes `.gitignore`, initializes Git, commits, and pushes

- `generate_env_example()`
  - Writes `.env.example` based on selected features

- `run_wizard()`
  - Drives the interactive CLI flow

- `handle_external_source()`
  - Loads a template from a `source:` repository URL

## 13. Behavior Summary

At a high level, Project Creator does three things:

1. Creates a numbered project folder.
2. Scaffolds files and directories based on your chosen mode.
3. Optionally turns the folder into a Git repository and pushes it.

That makes it suitable for quickly starting a new repo without repeating the same setup work every time.

## 14. Current Limitations

The current implementation has a few practical limitations worth knowing:

- The project name is converted by replacing spaces with hyphens only. It does not perform deep sanitization.
- `handle_external_source()` expects a `source:` string in a very specific format.
- Cloud template mode assumes the GitHub repository structure matches the hardcoded `templates/` layout.
- The code checks for `python` on `PATH`, which is fine on many systems but can vary by platform installation.

These are not necessarily bugs, but they are important implementation details for users and contributors.

## 15. License

See [`LICENSE`](../LICENSE).
