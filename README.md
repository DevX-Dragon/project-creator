# Project Creator
I built Project Architect because I was tired of manually creating the same folder structures, initializing git, and setting up virtual environments every time I started a new engineering project. This tool automates the "boring stuff" so you can get straight to the actual design and code.

## Why?
When you are going to be switching between KiCad, Firmware, and Web Development having a proper structured folder is a pain. This app ensures that each and every project is consistent numbered hierarchy without you worrying about it.

## What it does?
- **Project Numbering**: It looks at your current directory and automatically picks the next available number.

- **Selectable Folder Templates**: Give options to choose what folders have to be created according to user input.

- **Base Files**: Creates the basic `.kicad_pro` and `.kicad_sch` for KiCAD and basic `index.html`,`script.js` and `style.css` for web development.

- **Git Automation**: It handles the git init, creates the main branch, sets a remote orgin (orgin or an upstream based on user input), and performs your initial commit and push in one click.

## Security Concerns
This project does not have access to any of your git credentials. This script only runs the git commands for you via the terminal.

###### Fully built by **@DevX-Dragon**. A 14 year old developer from Sri Lanka 🇱🇰