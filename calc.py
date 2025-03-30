import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def click(event):
    """
    Handles button click events for the calculator.

    This function updates the calculator's display based on the button text.
    If the "=" button is clicked, it evaluates the expression in the display
    and updates the display with the result or an error message if the evaluation fails.
    If the "C" button is clicked, it clears the display.
    For all other buttons, it appends the button text to the display.

    Parameters:
    event (tkinter.Event): The event object containing information about the button click.
    """

    global scvalue
    text = event.widget.cget("text")
    if text == "=":
        try:
            value = eval(scvalue.get())
        except Exception:
            root.withdraw()
            scvalue.set("")
            messagebox.showerror("🤣🤣🤣🤣🤣🤣🤣🤣🤣", "Invalid Input. You are dumb at maths!")
            root.deiconify()
        scvalue.set(value)
    elif text == "C":
        scvalue.set("")
    else:
        scvalue.set(scvalue.get() + text)

# Main Window
root = tk.Tk()
root.title("Simple Calculator")

# Configure grid to make the "=" button fill the vertical space
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

# Entry Field for Display
scvalue = tk.StringVar()
scvalue.set("")
screen = ttk.Entry(root, textvariable=scvalue, font="lucida 15", justify="right")
screen.grid(row=0, column=0, columnspan=4, pady=10, padx=10, ipadx=10, ipady=15)

# Setting up the Style for Buttons
style = ttk.Style()
style.configure("TButton", font=("Lucida", 10))

# Buttons Layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", ".", "+"]
]

# Add buttons to grid
for i, row in enumerate(buttons):
    for j, text in enumerate(row):
        btn = ttk.Button(root, text=text, style="TButton")
        btn.grid(row=i + 1, column=j, padx=5, pady=5, ipadx=10, ipady=5)
        btn.bind("<Button-1>", click)

# Add "=" button spanning multiple rows
equals_button = ttk.Button(root, text="=", style="TButton")
equals_button.grid(row=1, column=4, rowspan=4, sticky="ns", padx=5, pady=5, ipadx=10, ipady=5)
equals_button.bind("<Button-1>", click)

root.mainloop()