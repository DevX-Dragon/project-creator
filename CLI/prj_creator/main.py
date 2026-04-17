#!/usr/bin/env python
import os
import re
import subprocess
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

def run_wizard():
    print(r"""
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
    
    [ PRJ-CREATOR ] Made by @devx-dragon
    ----------------------------------------------------------
    """)

    try:
        name = input("1. Project Name: ").strip().replace(" ", "-")
        if not name: return

        print("\n2. Modules (e.g., --web --hardware --venv --firmware --req)")
        selection = input("   Selection: ").lower()

        print("\n3. Select License")
        print("   [1] MIT | [2] GPL v3 | [3] None")
        lic_choice = input("   Choice: ")
        
        repo = input("\n4. Git URL (optional): ").strip()
        
        next_num = get_next_project_number()
        root_folder = f"{next_num:02d}.{name}"
        root_path = os.path.abspath(root_folder)
        
        print(f"\n[*] Initializing {root_folder}...")
        os.makedirs(root_path, exist_ok=True)
        os.makedirs(os.path.join(root_path, "images"), exist_ok=True)

        # License
        if lic_choice == "1":
            with open(os.path.join(root_path, "LICENSE"), "w") as f:
                f.write("MIT License\n\nCopyright (c) 2026 DevX-Dragon")
        
        # Firmware Logic
        if "--firmware" in selection:
            fw_path = os.path.join(root_path, "firmware")
            os.makedirs(fw_path, exist_ok=True)
            with open(os.path.join(fw_path, f"{name}.ino"), "w") as f:
                f.write(f"// {name} Firmware\nvoid setup() {{\n\n}}\n\nvoid loop() {{\n\n}}")
            print("   [+] Firmware directory created")

        # Requirements Logic
        if "--req" in selection:
            with open(os.path.join(root_path, "requirements.txt"), "w") as f:
                f.write("# Project dependencies\n")
            print("   [+] requirements.txt initialized")

        # Hardware Logic
        if "--hardware" in selection:
            hw_path = os.path.join(root_path, "hardware")
            os.makedirs(hw_path, exist_ok=True)
            print("   [+] Hardware directory created")

        # Web Logic
        if "--web" in selection:
            web_path = os.path.join(root_path, "web")
            os.makedirs(web_path, exist_ok=True)
            
            # HTML
            with open(os.path.join(web_path, "index.html"), "w") as f:
                f.write(f"<!DOCTYPE html>\n<html>\n<head>\n    <title>{name}</title>\n    <link rel='stylesheet' href='style.css'>\n</head>\n<body>\n    <h1>{name}</h1>\n    <script src='script.js'></script>\n</body>\n</html>")
            
            # CSS
            with open(os.path.join(web_path, "style.css"), "w") as f:
                f.write("body {\n    background: #000;\n    color: #fff;\n    font-family: monospace;\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    height: 100vh;\n}")
            
            # JS
            with open(os.path.join(web_path, "script.js"), "w") as f:
                f.write(f"console.log('{name} initialized.');")
            
            print("   [+] Web assets created (HTML/CSS/JS)")

        # Virtual Env Logic
        if "--venv" in selection:
            subprocess.run([sys.executable, "-m", "venv", os.path.join(root_path, "venv")], capture_output=True)
            print("   [+] Virtual environment initialized")

        # Git Logic
        if repo:
            subprocess.run(["git", "init"], cwd=root_path, capture_output=True)
            subprocess.run(["git", "remote", "add", "origin", repo], cwd=root_path, capture_output=True)
            print(f"   [+] Remote 'origin' set to {repo}")

        print(f"\n[!] Success. Workspace ready in {root_folder}")
        
    except Exception as e:
        print(f"\n[X] Error: {e}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    run_wizard()