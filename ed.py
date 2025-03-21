import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json  # Import JSON for saving and loading settings

SETTINGS_FILE = "settings.json"  # Path for the settings file

# Load settings from file
def load_settings():
    global current_font, current_size
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            current_font = settings.get("font", "Cascadia Mono")  # Default if not found
            current_size = settings.get("size", 14)  # Default if not found
    except FileNotFoundError:
        current_font = "Cascadia Mono"
        current_size = 14

# Save settings to file
def save_settings():
    settings = {
        "font": current_font,
        "size": current_size
    }
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)
    messagebox.showinfo("Settings", "Font settings saved successfully!")

# New file function
def new_file():
    if messagebox.askyesnocancel("Save File", "Do you want to save the current file before creating a new one?"):
        save_file()
    text_area.delete(1.0, tk.END)

# Open file function
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, file.read())

# Save file function
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        messagebox.showinfo("Save", "File saved successfully!")

# Exit editor function
def exit_editor():
    if messagebox.askyesnocancel("Save File", "Do you want to save the current file before exiting?"):
        save_file()
    root.destroy()

# Open settings function
def open_settings():
    def apply_settings():
        selected_font = font_var.get()
        selected_size = size_var.get()
        text_area.config(font=(selected_font, selected_size))
        
        global current_font, current_size
        current_font = selected_font
        current_size = selected_size
        
        save_settings()  # Save settings to the file
        settings_window.destroy()

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    settings_window.resizable(False, False)

    # Font Options
    ttk.Label(settings_window, text="Font:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    font_var = tk.StringVar(value=current_font)
    font_options = ttk.Combobox(settings_window, textvariable=font_var, values=["Cascadia Mono", "Arial", "Courier New", "Lucida Console"])
    font_options.grid(row=0, column=1, padx=10, pady=10)
    font_options.state(["readonly"])

    # Font Size Options
    ttk.Label(settings_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    size_var = tk.IntVar(value=current_size)
    size_spinbox = ttk.Spinbox(settings_window, from_=8, to=72, textvariable=size_var, width=5)
    size_spinbox.grid(row=1, column=1, padx=10, pady=10)

    # Apply Button
    apply_button = ttk.Button(settings_window, text="Apply", command=apply_settings)
    apply_button.grid(row=2, column=0, columnspan=2, pady=20)

# Main Window
root = tk.Tk()
root.title("ed - The Most Precise Text Editor")
root.geometry("800x600")

# Load font settings at startup
load_settings()

# Adding a Frame to Hold Text Area and Scrollbar
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True, padx=5, pady=5)

# Adding a Text Area
text_area = tk.Text(frame, wrap="word", font=(current_font, current_size), undo=True)
text_area.grid(row=0, column=0, sticky="nsew")

# Adding a Scrollbar and Attaching to Text Area
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_area.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_area.config(yscrollcommand=scrollbar.set)

# Configure grid weights to make everything expand properly
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Adding a Menu
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)
menu_bar.add_cascade(label="File", menu=file_menu)

# Adding Settings Option
menu_bar.add_command(label="Settings", command=open_settings)

root.config(menu=menu_bar)

root.mainloop()