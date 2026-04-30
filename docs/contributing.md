# Contributing Templates

Thanks for helping improve Project Creator.

This repo accepts template contributions through pull requests, especially for the `templates/` folder that powers the cloud template workflow.

## What To Contribute

You can open a pull request with:

- A new template folder
- An improvement to an existing template
- Fixes to generated starter files
- Small documentation updates that help explain a template

## Template Folder Rules

Please keep each template self-contained inside `templates/`.

Recommended layout:

```text
templates/
  your-template-name/
    files...
```

Guidelines:

- Use lowercase names with hyphens if possible
- Keep the folder name descriptive
- Include only the files needed for that template
- Make sure the template works when copied into a fresh project folder
- Avoid committing secrets, tokens, or machine-specific files

## Good Template Examples

A template may contain things like:

- starter HTML, CSS, and JavaScript files
- a Python app skeleton
- an Arduino or firmware scaffold
- documentation or test folders
- placeholder config files

## Before You Open a Pull Request

Please check that:

- The template opens and runs correctly after being downloaded
- File paths are correct
- File names are consistent
- The template does not depend on local-only setup
- The README or documentation needs are covered if the template has special steps

## Pull Request Tips

- Add a short description of what the template is for
- Include screenshots if the template has a visual result
- Mention any special setup or dependencies
- Say whether the template is new or an update to an existing one

## Reporting Problems

If a template is broken or downloads incorrectly, open an issue or a pull request with:

- The template name
- What you expected to happen
- What actually happened
- Any error message you saw

## Code Style

If you are editing project code as part of your contribution:

- Keep changes focused
- Follow the existing Python style
- Avoid unrelated cleanup in the same pull request

## Thank You

Template contributions help keep Project Creator useful for more kinds of projects. Small, well-made templates are especially welcome.
