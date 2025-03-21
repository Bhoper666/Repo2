import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, messagebox
import subprocess
import json
import os

# Save and load settings
SETTINGS_FILE = "settings_rterm.json"

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"font": ("Consolas", 12), "prompt": "> "}  # Default settings

# Function to handle commands
def execute_command():
    global command_log
    command = entry.get()[len(settings["prompt"]):]  # Remove the prompt indicator
    if command.strip():
        try:
            # Check if PowerShell or other tools need special handling
            if command.lower().startswith("powershell"):
                process = subprocess.Popen(["powershell", "-NoLogo", "-NoProfile", "-Command", command[10:]], 
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()
            else:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()

            # Display the output or error
            if output:
                terminal.insert(tk.END, f"{settings['prompt']}{command}\n{output}\n")
            if error:
                terminal.insert(tk.END, f"{settings['prompt']}{command}\n{error}\n")

            # Log the command and output
            command_log.append(f"{settings['prompt']}{command}\n{output}\n{error}\n")
        except Exception as e:
            terminal.insert(tk.END, f"Error: {e}\n")
        finally:
            entry.delete(0, tk.END)
            entry.insert(0, settings["prompt"])
            terminal.see(tk.END)  # Scroll to the bottom

# Export commands to a .log file
def export_log():
    file_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.writelines(command_log)
            messagebox.showinfo("Export", "Command log exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export log: {e}")

# Open settings menu
def open_settings():
    def apply_settings():
        try:
            # Update font and prompt settings
            font_family = font_var.get()
            font_size = int(size_var.get())
            settings["font"] = (font_family, font_size)
            settings["prompt"] = prompt_var.get()
            save_settings(settings)
            # Apply updated font to terminal and input
            terminal.config(font=settings["font"])
            entry.config(font=settings["font"])
            entry.delete(0, tk.END)
            entry.insert(0, settings["prompt"])
            settings_window.destroy()
        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to apply settings: {e}")

    # Create settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x200")

    # Font family selection
    tk.Label(settings_window, text="Font Family:").grid(row=0, column=0, padx=10, pady=10)
    font_var = tk.StringVar(value=settings["font"][0])
    tk.Entry(settings_window, textvariable=font_var).grid(row=0, column=1, padx=10, pady=10)

    # Font size selection
    tk.Label(settings_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=10)
    size_var = tk.StringVar(value=str(settings["font"][1]))
    tk.Entry(settings_window, textvariable=size_var).grid(row=1, column=1, padx=10, pady=10)

    # Prompt design
    tk.Label(settings_window, text="Prompt:").grid(row=2, column=0, padx=10, pady=10)
    prompt_var = tk.StringVar(value=settings["prompt"])
    tk.Entry(settings_window, textvariable=prompt_var).grid(row=2, column=1, padx=10, pady=10)

    # Save button
    tk.Button(settings_window, text="Save", command=apply_settings).grid(row=3, column=0, columnspan=2, pady=20)

# Load saved settings
settings = load_settings()
command_log = []

# Main application window
root = tk.Tk()
root.title("rterm - The Most Precise Terminal")
root.configure(bg="#282c34")
root.geometry("800x600")

# Menu bar with settings and export options
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Settings", command=open_settings)
file_menu.add_command(label="Export Log", command=export_log)
menu_bar.add_cascade(label="File", menu=file_menu)

# Terminal output area
terminal = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=settings["font"], bg="#1e1e1e", fg="#dcdcdc",
    insertbackground="#ffffff", height=25, width=80, state="normal"
)
terminal.pack(pady=(10, 0), padx=10, fill=tk.BOTH, expand=True)  # Fill both horizontally and vertically


# Command input area
entry = tk.Entry(
    root, font=settings["font"], bg="#1e1e1e", fg="#dcdcdc",
    insertbackground="#ffffff", relief="flat", width=80
)
entry.pack(pady=5, padx=10, fill=tk.X)
entry.insert(0, settings["prompt"])
entry.bind("<Return>", lambda event: execute_command())

# Focus the command input field on launch
entry.focus_set()

# Start the application
root.mainloop()