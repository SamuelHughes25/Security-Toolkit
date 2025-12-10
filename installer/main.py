import os
import json
import requests
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

# ----------------------------
# Constants
# ----------------------------
CLIENT_WIDTH = 315
CLIENT_HEIGHT = 245
STATIC_DIR = "static"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/SamuelHughes25/Security-Toolkit/main"
TOOLS_JSON_URL = f"{GITHUB_RAW_BASE}/tools.json"

# ----------------------------
# Functions (integrated from functions.py)
# ----------------------------
def download_tool(url, destination):
    """Download a tool from URL to a specified folder."""
    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded {destination} successfully")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def install_tool(tool_config, install_folder, silent=False):
    """
    Install a tool based on its configuration.
    tool_config: dict with keys 'name', 'url', 'type', 'category', 'silent_args' (optional)
    install_folder: where to download/install
    silent: whether to run in silent mode
    """
    tool_name = tool_config['name']
    tool_url = tool_config['url']
    tool_type = tool_config['type'].lower()
    
    # Determine file extension
    if tool_url.endswith('.msi'):
        ext = '.msi'
    elif tool_url.endswith('.exe'):
        ext = '.exe'
    else:
        ext = '.exe'  # default
    
    installer_path = os.path.join(install_folder, f"{tool_name.replace(' ', '_')}{ext}")
    
    # Handle static vs dynamic tools
    if tool_type == "static":
        # Static tool: should be in static/ directory or on GitHub
        local_static_path = os.path.join(STATIC_DIR, os.path.basename(tool_url))
        
        # Check if file exists locally
        if os.path.isfile(local_static_path):
            installer_path = local_static_path
            print(f"Using local static file: {installer_path}")
        else:
            # Try to download from GitHub
            github_static_url = f"{GITHUB_RAW_BASE}/static/{os.path.basename(tool_url)}"
            print(f"Downloading static file from GitHub: {github_static_url}")
            if not download_tool(github_static_url, installer_path):
                print(f"Failed to download static tool {tool_name}")
                return False
    
    elif tool_type == "dynamic":
        # Dynamic tool: download from the URL
        print(f"Downloading dynamic tool from: {tool_url}")
        if not download_tool(tool_url, installer_path):
            print(f"Failed to download dynamic tool {tool_name}")
            return False
    
    else:
        print(f"Unknown tool type: {tool_type}")
        return False
    
    # Build installation command
    try:
        if ext == '.msi':
            # MSI installer
            args = ["msiexec.exe", "/i", installer_path]
            if silent:
                args += ["/quiet", "/norestart"]
        else:
            # EXE installer
            args = [installer_path]
            if silent:
                # Check for custom silent args in tool config
                silent_args = tool_config.get('silent_args', '/S /silent /quiet')
                args += silent_args.split()
        
        print(f"Running installer: {' '.join(args)}")
        
        # Run the installer and wait for it to complete
        result = subprocess.run(args, check=True)
        print(f"{tool_name} installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Installation failed for {tool_name}: {e}")
        return False
    except Exception as e:
        print(f"Installation error for {tool_name}: {e}")
        return False

def load_tools_from_github():
    """Load tools configuration from GitHub or local JSON."""
    # Try loading from GitHub first
    try:
        response = requests.get(TOOLS_JSON_URL, timeout=10)
        response.raise_for_status()
        tools = response.json()
        print("Loaded tools from GitHub")
        return tools
    except Exception as e:
        print(f"Failed to load from GitHub: {e}")
    
    # Fall back to local tools.json if it exists
    local_json = "tools.json"
    if os.path.exists(local_json):
        try:
            with open(local_json, 'r') as f:
                tools = json.load(f)
                print("Loaded tools from local tools.json")
                return tools
        except Exception as e:
            print(f"Failed to load local tools.json: {e}")
    
    # Return default tools if both fail
    print("Using default tool configuration")
    return [
        {
            "name": "WinDirStat",
            "url": "static/WinDirStat-x64.msi",
            "type": "static",
            "category": "Maintenance"
        },
        {
            "name": "WinRAR",
            "url": "static/winrar-x64.exe",
            "type": "static",
            "category": "Maintenance"
        },
        {
            "name": "VLC Media Player",
            "url": "static/vlc-3.0.18.exe",
            "type": "static",
            "category": "Maintenance"
        },
        {
            "name": "Malwarebytes",
            "url": "https://data-cdn.mbamupdates.com/web/mb-windows/MBSetup.exe",
            "type": "dynamic",
            "category": "Security",
            "silent_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART"
        }
    ]

# ----------------------------
# Load tools configuration
# ----------------------------
ALL_TOOLS = load_tools_from_github()

# Organize tools by category
SECURITY_TOOLS = [t for t in ALL_TOOLS if t['category'].lower() == 'security']
MAINTENANCE_TOOLS = [t for t in ALL_TOOLS if t['category'].lower() == 'maintenance']

# ----------------------------
# Main Window
# ----------------------------
root = tk.Tk()
root.title("Security Toolkit Installer")
root.geometry(f"{CLIENT_WIDTH}x{CLIENT_HEIGHT}")
root.resizable(False, False)

# ----------------------------
# Stage frames
# ----------------------------
stage1 = tk.Frame(root, width=CLIENT_WIDTH, height=CLIENT_HEIGHT)
stage2 = tk.Frame(root, width=CLIENT_WIDTH, height=CLIENT_HEIGHT)
stage3 = tk.Frame(root, width=CLIENT_WIDTH, height=CLIENT_HEIGHT)

for frame in (stage1, stage2, stage3):
    frame.grid(row=0, column=0, sticky='nsew')
    frame.grid_propagate(False)

# ----------------------------
# Stage 1: Welcome
# ----------------------------
tk.Label(stage1, text="Welcome to Security Toolkit Installer", 
         font=("Segoe UI", 14), wraplength=300).pack(pady=40)

def goto_stage2():
    stage2.tkraise()

tk.Button(stage1, text="Continue", width=15, command=goto_stage2).pack(pady=20)

# ----------------------------
# Stage 2: App Selection
# ----------------------------
security_vars = {}
maintenance_vars = {}

# Create variables for each tool
for tool in SECURITY_TOOLS:
    security_vars[tool['name']] = tk.BooleanVar()

for tool in MAINTENANCE_TOOLS:
    maintenance_vars[tool['name']] = tk.BooleanVar()

# Dropdown toggle helper
def toggle(frame, arrow_label):
    if frame.winfo_viewable():
        frame.grid_remove()
        arrow_label.config(text="▶")
    else:
        frame.grid()
        arrow_label.config(text="▼")

# Security dropdown
sec_arrow = tk.Label(stage2, text="▼")
sec_arrow.grid(row=0, column=0, sticky='w', padx=5)
sec_label = tk.Label(stage2, text="Security Tools", font=("Segoe UI", 12, "bold"))
sec_label.grid(row=0, column=1, sticky='w')

sec_frame = tk.Frame(stage2)
for i, tool in enumerate(SECURITY_TOOLS):
    tk.Checkbutton(sec_frame, text=tool['name'], 
                   variable=security_vars[tool['name']]).grid(row=i, column=0, sticky='w')
sec_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=20)

def toggle_sec(event=None):
    toggle(sec_frame, sec_arrow)
sec_arrow.bind("<Button-1>", toggle_sec)
sec_label.bind("<Button-1>", toggle_sec)

# Maintenance dropdown
maint_arrow = tk.Label(stage2, text="▼")
maint_arrow.grid(row=2, column=0, sticky='w', padx=5)
maint_label = tk.Label(stage2, text="Maintenance Tools", font=("Segoe UI", 12, "bold"))
maint_label.grid(row=2, column=1, sticky='w')

maint_frame = tk.Frame(stage2)
for i, tool in enumerate(MAINTENANCE_TOOLS):
    tk.Checkbutton(maint_frame, text=tool['name'],
                   variable=maintenance_vars[tool['name']]).grid(row=i, column=0, sticky='w')
maint_frame.grid(row=3, column=0, columnspan=2, sticky='w', padx=20)

def toggle_maint(event=None):
    toggle(maint_frame, maint_arrow)
maint_arrow.bind("<Button-1>", toggle_maint)
maint_label.bind("<Button-1>", toggle_maint)

# ----------------------------
# Stage 3: Download Settings
# ----------------------------
silent_var = tk.BooleanVar()
notify_var = tk.BooleanVar()
shortcuts_var = tk.BooleanVar()

tk.Label(stage3, text="Download Settings", 
         font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky='w', pady=5, padx=5)

tk.Checkbutton(stage3, text="Automatic/Silent install", 
               variable=silent_var).grid(row=1, column=0, sticky='w', pady=2, padx=5)
tk.Checkbutton(stage3, text="Notify on completion", 
               variable=notify_var).grid(row=2, column=0, sticky='w', pady=2, padx=5)
tk.Checkbutton(stage3, text="Create desktop shortcuts", 
               variable=shortcuts_var).grid(row=3, column=0, sticky='w', pady=2, padx=5)

download_path_var = tk.StringVar()
download_path_var.set(os.path.join(os.path.expanduser("~"), "Downloads"))
download_label = tk.Label(stage3, text=f"Download location: {download_path_var.get()}", 
                          wraplength=300, font=("Segoe UI", 8))
download_label.grid(row=4, column=0, sticky='w', pady=5, padx=5)

def choose_location():
    path = filedialog.askdirectory()
    if path:
        download_path_var.set(path)
        download_label.config(text=f"Download location: {path}")

choose_btn_stage3 = tk.Button(stage3, text="Choose", width=15, command=choose_location)
choose_btn_stage3.place(x=CLIENT_WIDTH-5, y=CLIENT_HEIGHT-5-30, anchor='se')

start_btn_stage3 = tk.Button(stage3, text="Start Download", width=15)
start_btn_stage3.place(x=CLIENT_WIDTH-5, y=CLIENT_HEIGHT-5, anchor='se')

back_btn_stage3 = tk.Button(stage3, text="Back", width=10, command=lambda: stage2.tkraise())
back_btn_stage3.place(x=CLIENT_WIDTH-5, y=5, anchor='ne')

# ----------------------------
# Stage 2 → Stage 3 Button
# ----------------------------
def goto_stage3():
    selected_tools = []
    
    # Collect selected security tools
    for tool in SECURITY_TOOLS:
        if security_vars[tool['name']].get():
            selected_tools.append(tool)
    
    # Collect selected maintenance tools
    for tool in MAINTENANCE_TOOLS:
        if maintenance_vars[tool['name']].get():
            selected_tools.append(tool)
    
    if not selected_tools:
        messagebox.showwarning("No Selection", 
                              "Please select at least one application to continue.")
        return
    
    # Store selected tools for Stage 3
    stage3.selected_tools = selected_tools
    stage3.tkraise()

continue_btn_stage2 = tk.Button(stage2, text="Continue", width=15, command=goto_stage3)
continue_btn_stage2.place(x=CLIENT_WIDTH-5, y=CLIENT_HEIGHT-5, anchor='se')

# ----------------------------
# Stage 3 → Start Installation
# ----------------------------
def install_selected_apps_thread():
    """Run installations in a separate thread to prevent GUI freezing."""
    tools_to_install = getattr(stage3, "selected_tools", [])
    download_folder = download_path_var.get()
    is_silent = silent_var.get()
    
    successful = []
    failed = []
    
    for i, tool in enumerate(tools_to_install, 1):
        print(f"\n[{i}/{len(tools_to_install)}] Installing {tool['name']}...")
        try:
            success = install_tool(tool, download_folder, silent=is_silent)
            if success:
                successful.append(tool['name'])
            else:
                failed.append(tool['name'])
        except Exception as e:
            print(f"Error installing {tool['name']}: {e}")
            failed.append(tool['name'])
    
    # Show completion notification
    if notify_var.get():
        message = f"Installation complete!\n\n"
        message += f"Successful: {len(successful)}\n"
        message += f"Failed: {len(failed)}\n"
        if failed:
            message += f"\nFailed tools:\n" + "\n".join(f"- {name}" for name in failed)
        messagebox.showinfo("Installation Complete", message)

def install_selected_apps():
    """Start installation in a background thread."""
    tools_to_install = getattr(stage3, "selected_tools", [])
    
    if not tools_to_install:
        messagebox.showwarning("No Tools", "No tools selected for installation.")
        return
    
    # Disable button during installation
    start_btn_stage3.config(state='disabled', text="Installing...")
    
    # Start installation thread
    install_thread = Thread(target=install_selected_apps_thread, daemon=True)
    install_thread.start()
    
    # Re-enable button after a delay (or could monitor thread completion)
    def check_thread():
        if install_thread.is_alive():
            root.after(1000, check_thread)
        else:
            start_btn_stage3.config(state='normal', text="Start Download")
    
    root.after(1000, check_thread)

start_btn_stage3.config(command=install_selected_apps)

# ----------------------------
# Show Stage 1 initially
# ----------------------------
stage1.tkraise()
root.mainloop()