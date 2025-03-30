import math
import tkinter as tk
from tkinter import messagebox

def add():
    try:
        result = float(entry1.get()) + float(entry2.get())
        display_result(result)
    except ValueError:
        display_error()

def subtract():
    try:
        result = float(entry1.get()) - float(entry2.get())
        display_result(result)
    except ValueError:
        display_error()

def multiply():
    try:
        result = float(entry1.get()) * float(entry2.get())
        display_result(result)
    except ValueError:
        display_error()

def divide():
    try:
        divisor = float(entry2.get())
        if divisor == 0:
            display_error("Division by zero")
        else:
            result = float(entry1.get()) / divisor
            display_result(result)
    except ValueError:
        display_error()

def power():
    try:
        result = math.pow(float(entry1.get()), float(entry2.get()))
        display_result(result)
    except ValueError:
        display_error()

def sqrt():
    try:
        value = float(entry1.get())
        if value < 0:
            display_error("Square root of negative number")
        else:
            result = math.sqrt(value)
            display_result(result)
    except ValueError:
        display_error()

def logarithm():
    try:
        value = float(entry1.get())
        base = float(entry2.get())
        if value <= 0 or base <= 0:
            display_error("Logarithm inputs must be positive")
        else:
            result = math.log(value, base)
            display_result(result)
    except ValueError:
        display_error()

def sine():
    try:
        angle = float(entry1.get())
        result = math.sin(math.radians(angle))
        display_result(result)
    except ValueError:
        display_error()

def cosine():
    try:
        angle = float(entry1.get())
        result = math.cos(math.radians(angle))
        display_result(result)
    except ValueError:
        display_error()

def tangent():
    try:
        angle = float(entry1.get())
        result = math.tan(math.radians(angle))
        display_result(result)
    except ValueError:
        display_error()

def factorial():
    try:
        value = int(entry1.get())
        if value < 0:
            display_error("Factorial of negative number")
        else:
            result = math.factorial(value)
            display_result(result)
    except ValueError:
        display_error()

def display_result(result):
    result_label.config(text=f"Result: {result}")

def display_error(message="Invalid input"):
    messagebox.showerror("Error", message)

def clear_entries():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result_label.config(text="Result:")

root = tk.Tk()
root.title("Scientific Calculator")

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

entry1 = tk.Entry(frame, width=20)
entry1.grid(row=0, column=0, padx=5, pady=5)

entry2 = tk.Entry(frame, width=20)
entry2.grid(row=0, column=1, padx=5, pady=5)

result_label = tk.Label(root, text="Result:")
result_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

buttons = [
    ("Add", add),
    ("Subtract", subtract),
    ("Multiply", multiply),
    ("Divide", divide),
    ("Power", power),
    ("Square Root", sqrt),
    ("Logarithm", logarithm),
    ("Sine", sine),
    ("Cosine", cosine),
    ("Tangent", tangent),
    ("Factorial", factorial),
    ("Clear", clear_entries),
]

for i, (text, func) in enumerate(buttons):
    tk.Button(button_frame, text=text, command=func).grid(row=i // 3, column=i % 3, padx=5, pady=5)

root.mainloop()
