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
    
    [ PRJ-CREATOR ] v2.1.2 | Made by @devx-dragon
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

        with open(os.path.join(root_path, ".gitignore"), "w") as f:
            f.write("venv/\n__pycache__/\n*.pyc\n.DS_Store\n*.log\ndist/\n")

        if lic_choice == "1":
            with open(os.path.join(root_path, "LICENSE"), "w") as f:
                f.write(f"MIT License\n\nCopyright (c) {time.strftime('%Y')} DevX-Dragon")
        elif lic_choice == "2":
            with open(os.path.join(root_path, "LICENSE"), "w") as f:
                f.write(f"GPL v3 License\n\nCopyright (c) {time.strftime('%Y')} DevX-Dragon")
        
        if "--firmware" in selection:
            fw_path = os.path.join(root_path, "firmware")
            os.makedirs(fw_path, exist_ok=True)
            with open(os.path.join(fw_path, f"{name}.ino"), "w") as f:
                f.write(f"void setup() {{}}\nvoid loop() {{}}")
            print("   [+] Firmware directory created")

        if "--req" in selection:
            with open(os.path.join(root_path, "requirements.txt"), "w") as f:
                f.write("# Project dependencies\n")
            print("   [+] requirements.txt initialized")

        if "--hardware" in selection:
            hw_path = os.path.join(root_path, "hardware")
            os.makedirs(hw_path, exist_ok=True)
            print("   [+] Hardware directory created")

        if "--web" in selection:
            web_path = os.path.join(root_path, "web")
            os.makedirs(web_path, exist_ok=True)
            with open(os.path.join(web_path, "index.html"), "w") as f:
                f.write(f"<!DOCTYPE html>\n<html>\n<head>\n    <title>{name}</title>\n    <link rel='stylesheet' href='style.css'>\n</head>\n<body>\n    <h1>{name}</h1>\n    <script src='script.js'></script>\n</body>\n</html>")
            with open(os.path.join(web_path, "style.css"), "w") as f:
                f.write("body { background: #000; color: #fff; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; }")
            with open(os.path.join(web_path, "script.js"), "w") as f:
                f.write(f"console.log('{name} initialized.');")
            print("   [+] Web assets created")

        if "--venv" in selection:
            print("   [*] Creating Virtual Environment...")
            subprocess.run([sys.executable, "-m", "venv", os.path.join(root_path, "venv")], capture_output=True)
            print("   [+] venv initialized")

        if repo:
            print("   [*] Pushing to GitHub (Branch: main)...")
            subprocess.run(["git", "init"], cwd=root_path, capture_output=True)
            subprocess.run(["git", "remote", "add", "origin", repo], cwd=root_path, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root_path, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=root_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit via prj-creator"], cwd=root_path, capture_output=True)
            result = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=root_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   [+] Successfully pushed to {repo}")
            else:
                print("   [!] Git push failed. Ensure remote is empty and you are authenticated.")

        print(f"\n[!] Success. Workspace ready in {root_folder}")
        
    except Exception as e:
        print(f"\n[X] Error: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    run_wizard()