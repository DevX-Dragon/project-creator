#!/usr/bin/env python
import os
import re
import json
import shutil
import subprocess
import sys
import argparse
import requests
from git import Repo 
from rich.console import Console 
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from colorama import init, Fore, Style, just_fix_windows_console
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

just_fix_windows_console()
init(autoreset=True)
console = Console()

DEFAULT_USER = "DevX-Dragon"
DEFAULT_REPO = "project-creator"
VERSION = "3.0.1"

def get_template_dirs(user, repo):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/templates"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError("GitHub API did not return a template directory list.")

    return [item["name"] for item in payload if item.get("type") == "dir" and "name" in item]

def check_system_health():
    tools = ["git", "python", "pip"]
    missing = []
    for tool in tools:
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        console.print(f"[bold red][!] Missing system dependencies: {', '.join(missing)}[/bold red]")
        sys.exit(1)

def fix_terminal():
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        os.system('chcp 65001 > nul')

def get_header():
    art = r"""
    ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
    ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   
    ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   
    ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   
                                                              
     ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗ 
    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
    ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    """
    return Panel(f"[magenta]{art}[/magenta]", title=f"[bold cyan]v{VERSION}[/bold cyan]", subtitle="[bold magenta]@devx-dragon[/bold magenta]", border_style="bright_magenta")

def get_next_num():
    max_num = 0
    try:
        folders = [d for d in os.listdir('.') if os.path.isdir(d)]
        for f in folders:
            match = re.match(r'^(\d+)\.', f)
            if match:
                n = int(match.group(1))
                if n > max_num: max_num = n
    except: pass
    return max_num + 1

def download_remote_folder(user, repo, repo_path, local_dest):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{repo_path}"
    response = requests.get(url)
    if response.status_code != 200: return
    items = response.json()
    if not os.path.exists(local_dest): os.makedirs(local_dest)
    for item in items:
        if item['type'] == 'dir':
            download_remote_folder(user, repo, item['path'], os.path.join(local_dest, item['name']))
        else:
            file_data = requests.get(item['download_url']).content
            with open(os.path.join(local_dest, item['name']), 'wb') as f: f.write(file_data)

def handle_git_logic(root_path, repo_urls, selected):
    ignore_path = os.path.join(root_path, ".gitignore")
    content = "__pycache__/\n*.pyc\n.env\n"
    if "venv" in selected: content += "venv/\n"
    with open(ignore_path, "w") as f: f.write(content)

    repo = Repo.init(root_path)
    repo.git.branch("-M", "main")
    repo.index.add([".gitignore"] + [f for f in os.listdir(root_path) if f != ".git"])
    repo.index.commit(f"Initial commit (Project Creator v{VERSION})")
    console.print("[green][+] Git initialized and initial commit created on 'main'.[/green]")

    if repo_urls:
        urls = [url.strip() for url in repo_urls.split(",")]
        for i, url in enumerate(urls):
            remote_name = "origin" if i == 0 else f"remote-{i}"
            origin = repo.create_remote(remote_name, url)
            
            do_push = inquirer.confirm(message=f"Push to {remote_name} ({url})?", default=True).execute()
            if do_push:
                with console.status(f"[bold yellow]Pushing to {remote_name}..."):
                    try:
                        origin.push(refspec='main:main', set_upstream=(i==0))
                        console.print(f"[bold green][SUCCESS] Pushed to {remote_name}![/bold green]")
                    except Exception as e:
                        console.print(f"[bold red][!] Push to {remote_name} failed: {e}[/bold red]")

def generate_env_example(root_path, selected):
    env_vars = ["DEBUG=True", "SECRET_KEY=generate_me_here"]
    if "api" in selected:
        env_vars.extend(["DATABASE_URL=sqlite:///./test.db", "PORT=8000"])
    if "web" in selected:
        env_vars.extend(["API_BASE_URL=http://localhost:8000"])
    
    with open(os.path.join(root_path, ".env.example"), "w") as f:
        f.write("\n".join(env_vars))
    console.print("[cyan][+] Generated .env.example with placeholders.[/cyan]")

def run_wizard():
    check_system_health()
    fix_terminal()
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(get_header())

    try:
        name = input(Fore.GREEN + "[?] " + Style.RESET_ALL + "Project Name: ").strip().replace(" ", "-")
        if not name: return

        mode = inquirer.select(
            message="Main Menu:",
            choices=[
                Choice("manual", name="1. Manual Setup (Toggle + Warm)"),
                Choice("cloud", name="2. Load Templates (Default Cloud)"),
                Choice("empty", name="3. Empty Repository"),
                "Exit"
            ],
            pointer=">>"
        ).execute()

        if mode == "Exit": return

        next_n = get_next_num()
        root_folder = f"{next_n:02d}.{name}"
        root_path = os.path.abspath(root_folder)

        if mode == "manual":
            os.system('cls' if os.name == 'nt' else 'clear')
            console.print(get_header())
            selected = inquirer.checkbox(
                message="Toggle Features (Space to select, Enter to build):",
                choices=[
                    Choice("web", name="Web (HTML/CSS/JS)"),
                    Choice("venv", name="Python Venv + Warming"),
                    Choice("api", name="FastAPI Backend"),
                    Choice("firm", name="Arduino Firmware"),
                    Choice("docs", name="Docs Folder"),
                    Choice("tests", name="PyTest Directory"),
                ],
                pointer=">>",
                enabled_symbol="[x]",
                disabled_symbol="[ ]"
            ).execute()

            os.makedirs(root_path, exist_ok=True)
            
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description="Architecting folders...", total=None)
                if "web" in selected:
                    wp = os.path.join(root_path, "web")
                    os.makedirs(wp, exist_ok=True)
                    for f in ["index.html", "style.css", "main.js"]: open(os.path.join(wp, f), 'w').close()
                if "api" in selected:
                    ap = os.path.join(root_path, "api")
                    os.makedirs(ap, exist_ok=True)
                    with open(os.path.join(ap, "main.py"), "w") as f: f.write("from fastapi import FastAPI\napp = FastAPI()")
                
                if "venv" in selected:
                    progress.add_task(description="Warming environment...", total=None)
                    subprocess.run([sys.executable, "-m", "venv", os.path.join(root_path, "venv")], capture_output=True)
                    if "api" in selected:
                        pip_ext = "Scripts/pip" if os.name == 'nt' else "bin/pip"
                        subprocess.run([os.path.join(root_path, "venv", pip_ext), "install", "fastapi", "uvicorn"], capture_output=True)
                
                if "firm" in selected:
                    fp = os.path.join(root_path, "firmware")
                    os.makedirs(fp, exist_ok=True)
                    with open(os.path.join(fp, f"{name}.ino"), "w") as f: f.write("void setup(){}\nvoid loop(){}")
                if "docs" in selected: os.makedirs(os.path.join(root_path, "docs"), exist_ok=True)
                if "tests" in selected: os.makedirs(os.path.join(root_path, "tests"), exist_ok=True)

            generate_env_example(root_path, selected)
            blueprint = {"name": name, "features": selected, "version": VERSION}
            with open(os.path.join(root_path, "blueprint.json"), "w") as f: json.dump(blueprint, f, indent=4)

        elif mode == "cloud":
            try:
                with console.status("[bold yellow]Syncing with Dragon Vault..."):
                    cloud_options = get_template_dirs(DEFAULT_USER, DEFAULT_REPO)
            except Exception as e:
                console.print(f"[bold red][!] Could not load cloud templates: {e}[/bold red]")
                return
            temp_choice = inquirer.select(message="Select Cloud Template:", choices=cloud_options).execute()
            download_remote_folder(DEFAULT_USER, DEFAULT_REPO, f"templates/{temp_choice}", root_path)
            selected = ["cloud-template"]

        elif mode == "empty":
            os.makedirs(root_path, exist_ok=True)
            with open(os.path.join(root_path, "README.md"), "w") as f: f.write(f"# {name}")
            selected = ["empty"]

        repo_urls = input(Fore.GREEN + "\n[?] " + Style.RESET_ALL + "Git Remote URL(s) (Optional, comma-separated): ").strip()
        handle_git_logic(root_path, repo_urls, selected)

        console.print(f"\n[bold green][SUCCESS] {root_folder} is ready.[/bold green]")
        
        if os.name == 'nt': os.startfile(root_path)
        else: subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", root_path])

    except Exception as e:
        console.print(f"\n[bold red][CRITICAL ERROR] {e}[/bold red]")
    
    input(f"\n{Fore.WHITE}{Style.DIM}Press Enter to Exit...")

def handle_external_source(source_str):
    try:
        url_part = source_str.split("source:")[1]
        parts = url_part.strip("/").split("/")
        user, repo = parts[-2], parts[-1]
        fix_terminal()
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(get_header())
        try:
            with console.status(f"[bold yellow][*] Fetching External Vault: {user}/{repo}"):
                options = get_template_dirs(user, repo)
        except Exception as e:
            console.print(f"[bold red][ERROR] Could not load external templates: {e}[/bold red]")
            return
        selected_temp = inquirer.select(message="Select Template:", choices=options).execute()
        name = input(Fore.GREEN + "[?] Project Name: ").strip().replace(" ", "-")
        dest = os.path.abspath(name)
        download_remote_folder(user, repo, f"templates/{selected_temp}", dest)
        console.print("[bold green][+] Deployed successfully.[/bold green]")
        if os.name == 'nt': os.startfile(dest)
    except Exception as e:
        console.print(f"[bold red][ERROR] {e}[/bold red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", help="source:https://github.com/user/repo")
    args = parser.parse_args()

    if args.command and "source:" in args.command:
        handle_external_source(args.command)
    else:
        run_wizard()
