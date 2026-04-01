# 🐉 Project Architect

A Python-based automation tool for developers. It generates project folders, configures Git, and pushes to GitHub in one click.

## 🚀 Key Features
- **Auto-Increment**: Detects existing project numbers and increments them.
- **Module Selection**: Toggle PCB, Firmware, and CAD folders.
- **Modern Git**: Uses `main` branch instead of `master`.
- **Remote Integration**: Supports both `origin` and `upstream` naming conventions.
- **Instant Push**: Automatically pushes the initial `.gitignore` so you can do `git push` immediately.

## 🛠️ Requirements
- **Python 3.x**
- **Git** (Must be in your System PATH)

## ⚠️ Important Note
For the **Initialize & Push** feature to work, the GitHub repository you link must be **completely empty** (no README or License created on GitHub).

###### This is mainly made for Hack Club Students who make hardware projects