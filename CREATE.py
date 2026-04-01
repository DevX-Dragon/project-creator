import os
import re
import subprocess
import tkinter as tk
from tkinter import messagebox

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
    except Exception:
        pass
    return max_num + 1

def create_project():
    project_name = name_entry.get().strip()
    repo_url = repo_entry.get().strip()
    
    if not project_name:
        messagebox.showwarning("Input Error", "Please enter a project name.")
        return

    next_num = get_next_project_number()
    root_folder = f"{next_num}.{project_name}"

    try:
        # 1. Create Folder Structure
        os.makedirs(root_folder, exist_ok=True)
        subfolders = ["images", "cart"]
        if pcb_var.get(): subfolders.append(f"{project_name} - kicad")
        if firmware_var.get(): subfolders.append("firmware")
        if cad_var.get(): subfolders.append("3D")

        for sub in subfolders:
            os.makedirs(os.path.join(root_folder, sub), exist_ok=True)
        
        # 2. Write .gitignore
        gitignore_path = os.path.join(root_folder, ".gitignore")
        with open(gitignore_path, "w") as f:
            f.write("# DevX-Dragon Project Template\n/cart/\n__pycache__/\n*.bak\n*.kicad_pcb-bak\n.DS_Store\n")
        
        # 3. Git Automation
        git_log = ""
        if repo_url:
            try:
                # Basic Init
                subprocess.run(["git", "init"], cwd=root_folder, check=True, capture_output=True)
                subprocess.run(["git", "branch", "-M", "main"], cwd=root_folder, check=True, capture_output=True)
                
                # Link Remote
                remote_name = "upstream" if upstream_mode_var.get() else "origin"
                subprocess.run(["git", "remote", "add", remote_name, repo_url], 
                               cwd=root_folder, check=True, capture_output=True)
                
                # Commit
                subprocess.run(["git", "add", "."], cwd=root_folder, check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", "Initial commit via Project Architect"], 
                               cwd=root_folder, check=True, capture_output=True)
                
                # --- THE FIX: Push and Set Upstream ---
                # This makes 'git push' work immediately afterward
                subprocess.run(["git", "push", "-u", remote_name, "main"], 
                               cwd=root_folder, check=True, capture_output=True)
                
                git_log = f"\nGit: Initialized, Committed, and Pushed to {remote_name}/main."
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode()
                git_log = f"\nWarning: Git setup partially failed. Check if repo is empty.\nError: {error_msg}"
        else:
            # Local only init
            subprocess.run(["git", "init"], cwd=root_folder, check=True, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root_folder, check=True, capture_output=True)
            git_log = "\nGit: Local 'main' branch initialized."

        messagebox.showinfo("Success", f"Project {next_num} Created!{git_log}")
        root.destroy()
        
    except Exception as e:
        messagebox.showerror("Error", f"System Error: {e}")

# --- UI (v3.3) ---
root = tk.Tk()
root.title("Project Architect v3.3")
root.geometry("400x440")
root.configure(padx=25, pady=25)

tk.Label(root, text="PROJECT IDENTITY", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
name_entry = tk.Entry(root, font=("Consolas", 11), width=40)
name_entry.pack(pady=(2, 15))
name_entry.focus_set()

tk.Label(root, text="REPOSITORY URL", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
repo_entry = tk.Entry(root, font=("Consolas", 10), width=40)
repo_entry.pack(pady=(2, 5))

upstream_mode_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Set as Upstream (instead of Origin)", 
               variable=upstream_mode_var, font=("Arial", 8, "italic")).pack(anchor='w', pady=(0, 15))

pcb_var, firmware_var, cad_var = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
tk.Label(root, text="MODULES", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
frame = tk.Frame(root)
frame.pack(pady=5, fill='x')
tk.Checkbutton(frame, text="PCB (KiCad)", variable=pcb_var).pack(anchor='w')
tk.Checkbutton(frame, text="Firmware", variable=firmware_var).pack(anchor='w')
tk.Checkbutton(frame, text="CAD (3D)", variable=cad_var).pack(anchor='w')

btn = tk.Button(root, text="INITIALIZE & PUSH", command=create_project, 
                bg="#1a1a1a", fg="white", font=("Arial", 10, "bold"), 
                height=2, cursor="hand2")
btn.pack(fill='x', pady=25)

root.mainloop()