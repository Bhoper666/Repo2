import tkinter as tk
from tkinter import messagebox

def get_ads():
    root.configure(bg="red")
    messagebox.showerror("ВАШ ПК ЗАРАЖЕНИЙ НАЙНЕБЕЗПЕЧНІШИМ ТРОЯНОМ!!!!!", "ВАШ ПК БУДЕ ЗНИЩЕНО ЗА 60 СЕКУНД!!!! ЩОБ ЗАПОБІГТИ ЦЬОМУ, НЕ НАТИСКАЙТЕ КНОПКУ ОК!!!!!!")
    exit()
def click_button(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(value))

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        root.configure(bg="red")
        messagebox.showerror("Помилка!", "Можливо, Ви неправильно обчислюєте! Помилка: " + str(e))
        root.configure(bg="#d9d9d9")

root = tk.Tk()
root.title("Калькулятор НЕ ДЛЯ ПУБЛІЧНОГО ВИКОРИСТАННЯ")

entry = tk.Entry(root, width=35, borderwidth=5, font=("Arial", 18))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

for (text, row, col) in buttons:
    if text == '=':
        tk.Button(root, text=text, width=10, height=2, command=calculate).grid(row=row, column=col)
    elif text == 'C':
        tk.Button(root, text=text, width=10, height=2, command=clear).grid(row=row, column=col)
    else:
        tk.Button(root, text=text, width=10, height=2, command=lambda t=text: click_button(t)).grid(row=row, column=col)

funnymsg = tk.Button(root, text="Реклама: Отримати рахунок Ілона Маска", command=get_ads)
funnymsg.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
root.mainloop()
