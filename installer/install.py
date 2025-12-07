import tkinter as tk
from tkinter import ttk, filedialog

# ----------------------------
# Main Window
# ----------------------------
root = tk.Tk()
root.title("Security Toolkit Installer")
root.geometry("450x350")  # smaller size to reduce whitespace
root.resizable(False, False)

# ----------------------------
# Stage frames
# ----------------------------
stage1 = tk.Frame(root)
stage2 = tk.Frame(root)
stage3 = tk.Frame(root)

for frame in (stage1, stage2, stage3):
    frame.grid(row=0, column=0, sticky='nsew')

# ----------------------------
# Stage 1: Welcome
# ----------------------------
tk.Label(stage1, text="Welcome to Security Toolkit Installer", font=("Segoe UI", 14)).pack(pady=40)
def goto_stage2():
    # Require at least one selection in stage2 before allowing stage3
    stage2.tkraise()
tk.Button(stage1, text="Continue", width=15, command=goto_stage2).pack(pady=20)

# ----------------------------
# Stage 2: App Selection
# ----------------------------
# Dictionaries: app name -> dummy download path
security_tools = ["Malwarebytes", "WinDirStat", "Recovery Toolbox"]
maintenance_tools = ["CCleaner", "Defraggler"]

# Variables for checkboxes
security_vars = {tool: tk.BooleanVar() for tool in security_tools}
maintenance_vars = {tool: tk.BooleanVar() for tool in maintenance_tools}

def toggle_frame(frame, arrow):
    if frame.winfo_ismapped():
        frame.grid_remove()
        arrow.config(text="▶")
    else:
        frame.grid()
        arrow.config(text="▼")

# Security Dropdown
sec_arrow = tk.Label(stage2, text="▼")
sec_arrow.grid(row=0, column=0, sticky='w')
tk.Label(stage2, text="Security Tools", font=("Segoe UI", 12, "bold")).grid(row=0, column=1, sticky='w')

sec_frame = tk.Frame(stage2)
sec_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=20)
for i, tool in enumerate(security_tools):
    tk.Checkbutton(sec_frame, text=tool, variable=security_vars[tool]).grid(row=i, column=0, sticky='w')

sec_arrow.bind("<Button-1>", lambda e: toggle_frame(sec_frame, sec_arrow))

# Maintenance Dropdown
maint_arrow = tk.Label(stage2, text="▼")
maint_arrow.grid(row=2, column=0, sticky='w')
tk.Label(stage2, text="Maintenance Tools", font=("Segoe UI", 12, "bold")).grid(row=2, column=1, sticky='w')

maint_frame = tk.Frame(stage2)
maint_frame.grid(row=3, column=0, columnspan=2, sticky='w', padx=20)
for i, tool in enumerate(maintenance_tools):
    tk.Checkbutton(maint_frame, text=tool, variable=maintenance_vars[tool]).grid(row=i, column=0, sticky='w')

maint_arrow.bind("<Button-1>", lambda e: toggle_frame(maint_frame, maint_arrow))

# Continue button (requires at least one selection)
def goto_stage3():
    if not any(var.get() for var in list(security_vars.values()) + list(maintenance_vars.values())):
        tk.messagebox.showwarning("Select at least one", "Please select at least one application to continue.")
        return
    stage3.tkraise()

tk.Button(stage2, text="Continue", width=15, command=goto_stage3).grid(row=4, column=1, sticky='e', pady=15)

# ----------------------------
# Stage 3: Download Settings
# ----------------------------
settings = ["Automatic/Silent download", "Notify on completion", "Create desktop shortcuts"]
checkbox_vars_stage3 = []

tk.Label(stage3, text="Download Settings", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky='w', pady=5)
for i, s in enumerate(settings):
    var = tk.BooleanVar()
    tk.Checkbutton(stage3, text=s, variable=var).grid(row=i+1, column=0, sticky='w', pady=2)
    checkbox_vars_stage3.append(var)

# Download location
download_path_var = tk.StringVar()
tk.Label(stage3, text="Download location:").grid(row=len(settings)+1, column=0, sticky='w', pady=5)
def choose_location():
    path = filedialog.askdirectory()
    if path:
        download_path_var.set(path)
tk.Button(stage3, text="Choose", width=15, command=choose_location).grid(row=len(settings)+1, column=1, sticky='w')

# Start Download and Back buttons
tk.Button(stage3, text="Start Download", width=15).grid(row=len(settings)+2, column=1, sticky='e', pady=10)
tk.Button(stage3, text="Back", width=10, command=lambda: stage2.tkraise()).grid(row=0, column=1, sticky='e')

# ----------------------------
# Show Stage 1 initially
# ----------------------------
stage1.tkraise()
root.mainloop()
