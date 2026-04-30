# Devlog

This devlog covers the work done after the `v2.1.3` release of Project Creator.

## After v2.1.3

### 2026-04-19 to 2026-04-29

After the last release, I turned Project Creator from a mostly functional CLI into a much more complete project scaffolding tool.

## What Changed

### Documentation overhaul

- Rewrote the main `README.md` into a more useful project overview
- Added a full software guide in `docs/Documentation.md`
- Added a polished documentation landing page in `docs/index.html`
- Added `CONTRIBUTING.md` so template contributions are easier
- Added `CHANGELOG.md` to track release history more clearly

### CLI improvements

- Expanded the CLI into a clearer numbered project scaffolding flow
- Added support for multiple setup modes:
  - Manual Setup
  - Load Templates
  - Empty Repository
- Added support for:
  - `web`
  - `venv`
  - `api`
  - `firm`
  - `docs`
  - `tests`
- Added generation of `.env.example`
- Added generation of `blueprint.json`
- Improved Git initialization and push behavior
- Switched the generated Git branch flow to `main`

### Template system

- Added bundled starter templates:
  - `basic-web`
  - `npm-package`
  - `python-pypi`
- Added template documentation for the bundled templates
- Added support for downloading templates from GitHub
- Added external template loading through `source:https://...`

### Project structure cleanup

- Expanded the repo layout to separate docs, templates, and CLI code more clearly
- Marked the old GUI version as discontinued and moved it into an archive-style folder
- Cleaned up older release-era code and documentation so the project feels more consistent

## Why It Mattered

The biggest improvement was making the project feel like a real reusable tool instead of just a small script.

Before this stretch of work, the project was mostly about creating folders and doing a basic Git push. After this stretch, it can:

- scaffold different kinds of projects
- generate starter files
- download templates from GitHub
- document itself properly
- present itself more cleanly to new users

## Challenges

- Keeping the CLI simple while adding more setup options
- Making template downloads feel reliable
- Making Git automation less fragile
- Writing documentation that explains the tool clearly without overwhelming people

## Current Status

Project Creator now has:

- a clearer CLI workflow
- better docs
- reusable templates
- a more complete release structure

## Next Ideas

- add more templates
- improve validation for project names
- make generated metadata files optional
- keep polishing the docs and release notes
