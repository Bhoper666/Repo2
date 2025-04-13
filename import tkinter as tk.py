import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, messagebox, ttk
import subprocess
import json
import os
import sys  # Import sys
import threading # Import threading

# Use pty on Unix-like systems, pywinpty on Windows
if sys.platform.startswith('win'):
    import winpty
else:
    import pty
    import tty  # Needed for setting raw mode
    import select  # Needed for non-blocking I/O

interactive_process = None
master_fd = None  # For Unix-like systems to store the PTY master file descriptor


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

def read_from_pty():
    """Reads output from the PTY in a non-blocking way (Unix)."""
    global master_fd
    while True:
        try:
            rlist, _, _ = select.select([master_fd], [], [], 0.1)  # Timeout of 0.1 seconds
            if rlist:
                output = os.read(master_fd, 1024).decode("utf-8", errors="replace")
                root.after(0, lambda: update_terminal(output))  # Update on main thread
        except OSError:
            break  # PTY probably closed
        except Exception as e: # if smth goes wrong 
            print(e)

def update_terminal(text):
    """Updates the terminal with new text (thread-safe)."""
    terminal.insert(tk.END, text)
    terminal.see(tk.END)

# Function to handle commands
def execute_command():
    global command_log, interactive_process, master_fd
    command_with_prompt = entry.get()
    command = command_with_prompt[len(settings["prompt"]):]

    if command.strip():
        if interactive_process:  #If an interactive process is running.
            try:
                if sys.platform.startswith('win'):
                   interactive_process.write((command + "\n").encode()) # Encode to bytes!
                else:
                    os.write(master_fd, (command + "\n").encode()) # Write to the PTY
            except Exception as e:
                terminal.insert(tk.END, f"Error writing to process: {e}\n")

        else: # if no interactive process is running
            try:
                if sys.platform.startswith('win'):
                    interactive_process = winpty.PtyProcess.spawn([command])
                    def read_loop():
                        while True:
                            try:
                                data = interactive_process.read()
                                if not data:
                                    break
                                root.after(0, lambda d=data: update_terminal(d))
                            except EOFError:
                                break # process ended

                    threading.Thread(target=read_loop, daemon=True).start()

                else: # Unix-like
                    pid, master_fd = pty.fork()
                    if pid == pty.CHILD:
                        # Inside the child process (the one running the command)
                        os.execvp(command.split()[0], command.split())
                    else:
                        # Inside the parent process (rterm)
                        threading.Thread(target=read_from_pty, daemon=True).start()
            except Exception as e:
                terminal.insert(tk.END, f"Error: {e}\n")

        entry.delete(0, tk.END)
        entry.insert(0, settings["prompt"])

# Add logic to terminate interactive processes with the "exit" command:
def terminate_interactive_process():
    global interactive_process, master_fd
    if interactive_process:
        if sys.platform.startswith('win'):
             interactive_process.close()
        else:
            os.close(master_fd)
        interactive_process = None
        master_fd = None
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
entry.bind("<Return>", lambda event: execute_command() if entry.get().strip() != settings["prompt"] + "exit" else terminate_interactive_process())

# Focus the command input field on launch
entry.focus_set()

# Start the application
root.mainloop()