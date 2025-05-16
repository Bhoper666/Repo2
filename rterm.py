from sys import stdout
import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, messagebox, ttk
import subprocess
import json
import os

interactive_process = None

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
def clear_out():
    terminal.delete(1.0, tk.END)
def end_session():
    exit()

# Function to handle commands
def execute_command():
    global command_log, interactive_process
    command = entry.get()[len(settings["prompt"]):]  # Remove the prompt indicator

    if command.strip():
        if interactive_process:
            try:
                # Send input to the interactive subprocess
                interactive_process.stdin.write(command + "\n")
                interactive_process.stdin.flush()
                # Read output from the subprocess
                output = interactive_process.stdout.readline()  # Read one line at a time
                terminal.insert(tk.END, output)
                terminal.see(tk.END)
            except Exception as e:
                terminal.insert(tk.END, f"Error: {e}\n")
        else:
            try:
                # Check for interactive programs
                if command.lower() in ["python3", "powershell"]:
                    interactive_process = subprocess.Popen(
                        command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=True
                    )
                    terminal.insert(tk.END, f"Started interactive session: {command}\n")
                else:
                    # Run non-interactive commands
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout if result.returncode == 0 else result.stderr
                    terminal.insert(tk.END, f"{settings['prompt']}{command}\n{output}\n")

                # Log the command and output
                command_log.append(f"{settings['prompt']}{command}\n{output}\n")
            except Exception as e:
                terminal.insert(tk.END, f"Error: {e}\n")
            finally:
                entry.delete(0, tk.END)
                entry.insert(0, settings["prompt"])
                terminal.see(tk.END)

# Add logic to terminate interactive processes with the "exit" command:
def terminate_interactive_process():
    global interactive_process
    if interactive_process:
        interactive_process.terminate()
        interactive_process = None
        terminal.insert(tk.END, "Exited interactive session.\n")

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
from tkinter.font import families  # Import for font listing

def open_settings():
    def apply_settings():
        try:
            # Update font and prompt settings
            font_family = font_combobox.get()
            font_size = int(size_spinbox.get())
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
    settings_window.geometry("400x250")

    # Font family picker
    tk.Label(settings_window, text="Font Family:").grid(row=0, column=0, padx=10, pady=10)
    font_combobox = ttk.Combobox(settings_window, values=list(families()), state="readonly")
    font_combobox.set(settings["font"][0])  # Set current font as default
    font_combobox.grid(row=0, column=1, padx=10, pady=10)

    # Font size spinner
    tk.Label(settings_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=10)
    size_spinbox = tk.Spinbox(settings_window, from_=8, to=72, width=5)
    size_spinbox.delete(0, tk.END)
    size_spinbox.insert(0, settings["font"][1])  # Set current font size as default
    size_spinbox.grid(row=1, column=1, padx=10, pady=10)

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
file_menu.add_command(label="Export Logs", command=export_log)
file_menu.add_command(label="Clear output", command=clear_out)
file_menu.add_command(label="Finish session", command=end_session)
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
