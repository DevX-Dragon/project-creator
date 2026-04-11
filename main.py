import os
import re
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import base64


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

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def create_project():
    project_name = name_entry.get().strip()
    if project_name == "your-project-name" or not project_name:
        messagebox.showwarning("Input Error", "Enter valid project name.")
        return
    
    repo_url = repo_entry.get().strip()
    if repo_url == "https://github.com/user/repo": repo_url = ""

    next_num = get_next_project_number()
    root_folder = f"{next_num}.{project_name}"

    try:
        os.makedirs(root_folder, exist_ok=True)
        os.makedirs(os.path.join(root_folder, "images"), exist_ok=True)
        os.makedirs(os.path.join(root_folder, "cart"), exist_ok=True)

        with open(os.path.join(root_folder, "README.md"), "w") as f:
            f.write(f"# {project_name}\n\nInitialized via Architect.")

        if venv_var.get():
            subprocess.run(["python", "-m", "venv", "venv"], cwd=root_folder)

        if req_var.get():
            with open(os.path.join(root_folder, "requirements.txt"), "w") as f:
                f.write("pyserial\n")

        if web_var.get():
            w_p = os.path.join(root_folder, "web")
            os.makedirs(w_p, exist_ok=True)
            with open(os.path.join(w_p, "index.html"), "w") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head><link rel='stylesheet' href='style.css'></head>\n<body><h1>Project</h1><script src='script.js'></script></body></html>")
            with open(os.path.join(w_p, "style.css"), "w") as f:
                f.write("body { background: #f0f0f0; font-family: sans-serif; }")
            with open(os.path.join(w_p, "script.js"), "w") as f:
                f.write("console.log('Loaded');")

        if pcb_var.get():
            k_p = os.path.join(root_folder, f"{project_name}-kicad")
            os.makedirs(k_p, exist_ok=True)
            with open(os.path.join(k_p, f"{project_name}.kicad_pro"), "w") as f:
                f.write('{"meta": {"version": 1}}')
            with open(os.path.join(k_p, f"{project_name}.kicad_sch"), "w") as f:
                f.write(f'(kicad_sch (version 20211123) (generator eeschema) (uuid "{next_num}")\n(paper "A4")\n(title_block (title "{project_name}"))\n)')

        if firmware_var.get():
            f_p = os.path.join(root_folder, "firmware")
            os.makedirs(f_p, exist_ok=True)
            with open(os.path.join(f_p, "main.py"), "w") as f:
                f.write("print('Hello World')")

        if cad_var.get():
            os.makedirs(os.path.join(root_folder, "3D"), exist_ok=True)
        
        with open(os.path.join(root_folder, ".gitignore"), "w") as f:
            f.write(ignore_text.get("1.0", tk.END).strip())
        
        if repo_url:
            subprocess.run(["git", "init"], cwd=root_folder, check=True, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root_folder, check=True, capture_output=True)
            rem = "upstream" if upstream_var.get() else "origin"
            subprocess.run(["git", "remote", "add", rem, repo_url], cwd=root_folder, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=root_folder, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=root_folder, check=True, capture_output=True)
            subprocess.run(["git", "push", "-u", rem, "main"], cwd=root_folder, check=True, capture_output=True)
        else:
            subprocess.run(["git", "init"], cwd=root_folder, check=True, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=root_folder, check=True, capture_output=True)

        messagebox.showinfo("Success", f"Project {next_num} Created!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Project Creator v3.4")
icon_data = """
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
"""
try:
    img = tk.PhotoImage(data=icon_data)
    root.wm_iconphoto(True, img)
except Exception as e:
    print(f"Icon failed to load: {e}")
root.geometry("400x450")
root.resizable(False, False)

notebook = ttk.Notebook(root)
tab1 = tk.Frame(notebook, padx=20, pady=10)
tab2 = tk.Frame(notebook, padx=20, pady=10)
notebook.add(tab1, text=" Basic ")
notebook.add(tab2, text=" Advanced ")
notebook.pack(expand=True, fill="both")

# --- Tab 1: Basic ---
tk.Label(tab1, text="PROJECT IDENTITY", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
name_entry = PlaceholderEntry(tab1, placeholder="your-project-name", font=("Consolas", 11), width=38)
name_entry.pack(pady=(2, 10), anchor='w')

tk.Label(tab1, text="REPOSITORY URL", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
repo_entry = PlaceholderEntry(tab1, placeholder="https://github.com/user/repo", font=("Consolas", 10), width=42)
repo_entry.pack(pady=(2, 2), anchor='w')

upstream_var = tk.BooleanVar(value=False)
tk.Checkbutton(tab1, text="Set Upstream", variable=upstream_var, font=("Arial", 8, "italic")).pack(anchor='w', pady=(0, 10))

tk.Label(tab1, text="MODULES", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
pcb_var, firmware_var, cad_var, web_var = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=False)
tk.Checkbutton(tab1, text="PCB (KiCad)", variable=pcb_var).pack(anchor='w')
tk.Checkbutton(tab1, text="Firmware", variable=firmware_var).pack(anchor='w')
tk.Checkbutton(tab1, text="CAD (3D)", variable=cad_var).pack(anchor='w')
tk.Checkbutton(tab1, text="Website (HTML/CSS/JS)", variable=web_var).pack(anchor='w')

# --- Tab 2: Advanced ---
tk.Label(tab2, text="ENVIRONMENT", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w')
venv_var, req_var = tk.BooleanVar(value=False), tk.BooleanVar(value=True)
tk.Checkbutton(tab2, text="Create venv", variable=venv_var).pack(anchor='w')
tk.Checkbutton(tab2, text="Generate requirements.txt", variable=req_var).pack(anchor='w')

tk.Label(tab2, text=".GITIGNORE RULES", font=("Arial", 8, "bold"), fg="#555").pack(anchor='w', pady=(10, 0))
ignore_text = tk.Text(tab2, font=("Consolas", 9), height=7, width=45)
ignore_text.pack(pady=5)
ignore_text.insert("1.0", "/cart/\n__pycache__/\n*.bak\nbuild/\ndist/\n.DS_Store")

btn = tk.Button(root, text="INITIALIZE & PUSH", command=create_project, bg="#1a1a1a", fg="white", font=("Arial", 10, "bold"), height=2, cursor="hand2")
btn.pack(fill='x', padx=20, pady=(0, 15))

root.mainloop()
