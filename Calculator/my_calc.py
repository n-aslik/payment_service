import tkinter as tk
from tkinter import ttk, messagebox
from math import factorial, sin, cos, tan, sqrt, exp, log, degrees, radians, pi
import math

class ModernCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Modern Calculator")
        self.window.geometry("500x500")
        self.window.resizable(True, True)
        self.window.configure(bg="#2c3e50")
        self.window.iconphoto(True, tk.PhotoImage(file="C:/Users/Администратор/Documents/Python_folder/Calculator/calculator.png"))

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12), padding=5)
        self.style.configure('TLabel', background='#2c3e50', foreground='white')
        self.style.configure('TEntry', font=('Arial', 14))

        # Single input/display
        self.expression = tk.StringVar()
        self.result = tk.StringVar()
        self.current_mode = "normal"
        self.last_operation = None

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        title_label = ttk.Label(main_frame, text="Modern Calculator",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Input/Result display (single entry)
        self.display_entry = ttk.Entry(main_frame, textvariable=self.expression,
                                      font=('Arial', 18, 'bold'), justify='right', width=30)
        self.display_entry.grid(row=1, column=0, columnspan=4, pady=5, padx=5, sticky="we")

        # Result below
        result_entry = ttk.Entry(main_frame, textvariable=self.result,
                                state='readonly', width=30, font=('Arial', 14, 'bold'), justify='right')
        result_entry.grid(row=2, column=0, columnspan=4, pady=5, padx=(5, 0), sticky="we")

        # Normal mode buttons
        normal_frame = ttk.LabelFrame(main_frame, text="Basic Operations", padding="5")
        normal_frame.grid(row=3, column=0, columnspan=4, sticky="we", pady=10)

        buttons_normal = [
            ('7', '8', '9', '+'),
            ('4', '5', '6', '-'),
            ('1', '2', '3', '*'),
            ('0', '.', 'C', '/'),
            ('%', 'x²', '√', '='),
            ('⌫',)  # Backspace
        ]

        for i, row in enumerate(buttons_normal):
            for j, text in enumerate(row):
                if text == '=':
                    btn = ttk.Button(normal_frame, text=text, command=self.evaluate)
                elif text == 'C':
                    btn = ttk.Button(normal_frame, text=text, command=self.clear)
                elif text == '⌫':
                    btn = ttk.Button(normal_frame, text=text, command=self.backspace)
                else:
                    btn = ttk.Button(normal_frame, text=text,
                                     command=lambda t=text: self.append_input(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="we")

        # Scientific mode buttons
        self.sci_frame = ttk.LabelFrame(main_frame, text="Scientific Functions", padding="5")

        buttons_scientific = [
            ('sin', 'cos', 'tan', 'ctg'),
            ('x^y', 'n!', 'log', 'ln'),
            ('deg', 'rad', '1/x', 'e^x'),
            ('10^x', 'x³', 'π', '±')
        ]

        for i, row in enumerate(buttons_scientific):
            for j, text in enumerate(row):
                btn = ttk.Button(self.sci_frame, text=text,
                                 command=lambda t=text: self.scientific_operation(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="we")

        # Mode selector
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=5, column=0, columnspan=4, pady=10)

        ttk.Button(mode_frame, text="Normal", command=self.set_normal_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(mode_frame, text="Scientific", command=self.set_scientific_mode).pack(side=tk.LEFT, padx=5)

    def set_normal_mode(self):
        self.sci_frame.grid_forget()
        self.window.geometry("500x500")
        self.current_mode = "normal"

    def set_scientific_mode(self):
        self.sci_frame.grid(row=4, column=0, columnspan=4, sticky="we", pady=10)
        self.window.geometry("500x750")
        self.current_mode = "scientific"

    def append_input(self, text):
        expr = self.expression.get()
        # Map x², √, etc. to Python expression
        if text == 'x²':
            self.expression.set(expr + '**2')
        elif text == '√':
            self.expression.set(expr + f'sqrt({expr})')
        elif text == '%':
            self.expression.set(expr + '/100')
        else:
            self.expression.set(expr + text)
        self.result.set("")

    def backspace(self):
        expr = self.expression.get()
        self.expression.set(expr[:-1])
        self.result.set("")

    def clear(self):
        self.expression.set("")
        self.result.set("")

    def evaluate(self):
        expr = self.expression.get()
        try:
            # Replace custom functions/strings with Python equivalents
            expr = expr.replace('π', 'pi')
            expr = expr.replace('sqrt', 'sqrt')
            value = eval(expr, {**math.__dict__, 'sqrt': sqrt})
            self.result.set(f"{value:.8g}")
        except Exception as e:
            self.result.set("")
            messagebox.showerror("Error", str(e))

    def scientific_operation(self, op):
        try:
            expr = self.expression.get()
            if not expr and op not in ('π',):
                raise ValueError("Enter an expression or number first")

            # Try to safely evaluate the current entry if it's a number
            try:
                value = float(eval(expr, {**math.__dict__, 'sqrt': sqrt}))
            except:
                value = None

            result = None
            if op == 'sin':
                result = sin(math.radians(value))
            elif op == 'cos':
                result = cos(math.radians(value))
            elif op == 'tan':
                result = tan(math.radians(value))
            elif op == 'ctg':
                if tan(math.radians(value)) == 0:
                    raise ValueError("Undefined value")
                result = 1 / tan(math.radians(value))
            elif op == 'x^y':
                # Wait for further input, append "**"
                self.expression.set(expr + '**')
                return
            elif op == 'n!':
                if value is None or value < 0 or value != int(value):
                    raise ValueError("Factorial requires non-negative integer")
                result = factorial(int(value))
            elif op == 'log':
                result = math.log10(value)
            elif op == 'ln':
                result = math.log(value)
            elif op == 'deg':
                result = degrees(value)
            elif op == 'rad':
                result = radians(value)
            elif op == '1/x':
                result = 1 / value
            elif op == 'e^x':
                result = exp(value)
            elif op == '10^x':
                result = 10 ** value
            elif op == 'x³':
                result = value ** 3
            elif op == 'π':
                self.expression.set(expr + 'π')
                return
            elif op == '±':
                result = int(-value)
            else:
                raise ValueError("Unknown function")
            self.result.set(f"{result:.8g}")
            self.expression.set(str(result))
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Run calculator
calc = ModernCalculator()
calc.window.mainloop()
