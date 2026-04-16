#!/usr/bin/env python3
import os
import re
import subprocess
import platform
import time
import sys

def get_next_project_number():
    max_num = 0
    try:
        items = os.listdir('.')
        folders = [d for d in items if os.path.isdir(d)]
        for folder in folders:
            match = re.match(r'^(\d+)\.', folder)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num
    except Exception: pass
    return max_num + 1

def progress_bar(task_name, duration=3):
    print(f"   [*] {task_name}")
    bar_width = 40
    for i in range(bar_width + 1):
        percent = int((i / bar_width) * 100)
        bar = "█" * i + "-" * (bar_width - i)
        sys.stdout.write(f"\r       [{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / bar_width)
    print("\n")

def run_wizard():
    print(r"""
    ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
    ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   
    ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   
    ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝
    
    Made by @devx-dragon | CLI v1.0
    ----------------------------------------------------------
    """)

    try:
        name = input("1. Project Name: ").strip().replace(" ", "-")
        if not name: return

        print("\n2. Modules (e.g., --web --pcb --venv --cart)")
        selection = input("   Selection: ").lower()

        print("\n3. Select License")
        print("   [1] MIT | [2] GPL v3 | [3] None")
        lic_choice = input("   Choice: ")
        
        repo = input("\n4. Git URL (optional): ").strip()
        set_upstream = "n"
        if repo:
            set_upstream = input("   Set as upstream? (y/n): ").lower()
        
        next_num = get_next_project_number()
        root_folder = f"{next_num}.{name}"
        root_path = os.path.abspath(root_folder)
        
        print(f"\n[*] Initializing {root_folder}...")
        os.makedirs(root_path, exist_ok=True)
        os.makedirs(os.path.join(root_path, "images"), exist_ok=True)

        # License
        if lic_choice == "1":
            with open(os.path.join(root_path, "LICENSE"), "w") as f:
                f.write(f"MIT License\n\nCopyright (c) 2026 DevX-Dragon")
        elif lic_choice == "2":
            with open(os.path.join(root_path, "LICENSE"), "w") as f:
                f.write("GNU GENERAL PUBLIC LICENSE Version 3...")

        # README
        with open(os.path.join(root_path, "README.md"), "w") as f:
            f.write(f"# {name}\n\nInitialized via DevX CLI.")

        # Modules
        if "--pcb" in selection:
            k_path = os.path.join(root_path, f"{name}-kicad")
            os.makedirs(k_path, exist_ok=True)
            with open(os.path.join(k_path, f"{name}.kicad_pro"), "w") as f: f.write('{"meta": {"version": 1}}')
            with open(os.path.join(k_path, f"{name}.kicad_sch"), "w") as f:
                f.write(f'(kicad_sch (version 20211123) (generator eeschema)\n(uuid "{next_num}")\n(paper "A4"))')
            print("   [+] KiCad project created")

        if "--venv" in selection:
            progress_bar("Creating Virtual Environment")
            subprocess.run(["python", "-m", "venv", "venv"], cwd=root_path, capture_output=True)
            with open(os.path.join(root_path, "requirements.txt"), "w") as f:
                f.write("# Project dependencies\n")

        with open(os.path.join(root_path, ".gitignore"), "w") as f:
            f.write("/cart/\n__pycache__/\n*.bak\nvenv/\n")

        # Git
        if repo:
            print("   [*] Pushing git...")
            subprocess.run(["git", "init"], cwd=root_path, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=root_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=root_path, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root_path, capture_output=True)
            
            remote_name = "upstream" if set_upstream == "y" else "origin"
            subprocess.run(["git", "remote", "add", remote_name, repo], cwd=root_path, capture_output=True)
            subprocess.run(["git", "push", "-u", remote_name, "main"], cwd=root_path, capture_output=True)
            print(f"   [+] Synced to {remote_name}")

        print(f"\n[!] Success. Project ready at {root_folder}")
        
        if platform.system() == "Windows": os.startfile(root_path)
        elif platform.system() == "Darwin": subprocess.run(["open", root_path])
        else: subprocess.run(["xdg-open", root_path])

    except Exception as e:
        print(f"\n[X] Error: {e}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    run_wizard()