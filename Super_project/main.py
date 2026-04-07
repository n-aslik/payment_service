import tkinter as tk
from tkinter import ttk,messagebox

class CurrencyConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("618x340")
        self.window.title("Перевод валюты сомони на другие валюты")
        self.window.resizable(False, False)
        self.window.iconphoto(True, tk.PhotoImage(file="C:/Users/Администратор/Documents/Python_folder/Super_project/conv.png"))
        self.bg_image =tk.PhotoImage(file="C:/Users/Администратор/Documents/Python_folder/Super_project/conv_s.png", height=200)
        self.bg_logo = ttk.Label(self.window, image=self.bg_image)
        self.bg_logo.grid(row=3, column=3)
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Consolas', 8), padding=5)
        self.style.configure('TLabel', background='lightblue', foreground='black', font=('Consolas', 8))
        self.style.configure('TEntry', font=('Consolas', 8))

        # Input variable

        self.currency = tk.StringVar()
        self.result = tk.StringVar()
        
        self.create_widget()
        # Create widgets
    def create_widget(self):
        head_frame = ttk.Frame(self.window, padding="10", width=540, relief="solid")
        head_frame.grid(row=0, column=0, padx=3, sticky="nsew", columnspan=4)

        # change usd/rub/cny courses
        update_currencies_frame = ttk.Frame(self.window, padding="5", width=540, relief="groove")
        update_currencies_frame.grid(row=4, column=0, padx=3, sticky="we", columnspan=4)

        usd_lable = ttk.Label(update_currencies_frame, text="USD", width=10, anchor="center", relief="sunken")
        usd_lable.grid(row=0, column=0, sticky="nsew")

        self.usd_courses = ttk.Entry(update_currencies_frame)
        self.usd_courses.grid(row=0, column=1, sticky="nsew", padx = 5)

        rub_lable = ttk.Label(update_currencies_frame, text="RUB", width=10, anchor="center", relief="sunken")
        rub_lable.grid(row=0, column=2, sticky="nsew")

        self.rub_courses = ttk.Entry(update_currencies_frame)
        self.rub_courses.grid(row=0, column=3, sticky="nsew", padx = 5)

        cny_lable = ttk.Label(update_currencies_frame, text="CNY", width=10, anchor="center", relief="sunken")
        cny_lable.grid(row=0, column=4, sticky="nsew")

        self.cny_courses = ttk.Entry(update_currencies_frame)
        self.cny_courses.grid(row=0, column=5, sticky="nsew", padx = 5)

        ##################################################################################################

        keyboard_frame = ttk.Frame(self.window, padding="20", width=540, relief="groove")
        keyboard_frame.grid(row = 3, column = 0, pady=10, padx=20, columnspan=3, sticky='ew')
        currency_buttons = [
            ('7', '8', '9'),
            ('4', '5', '6'),
            ('1', '2', '3'),
            ('0', '.', 'C'),
            ('USD','RUB', 'CNY'),
            ('⌫',) # Backspace
        ]
        # Labels
        current = ttk.Label(head_frame, text="Текущая валюта(TJS)", relief="ridge")
        current.grid(row=1, column=1, sticky="ew", padx=70)

        result = ttk.Label(head_frame, text = "Переведенная валюта(USD/RUB/CNY)", relief="ridge")
        result.grid(row=1, column=2, sticky='ew', padx=40)

        # Input currency 

        self.input = ttk.Entry(head_frame, textvariable=self.currency, font=('Consolas',8,'normal'), justify='right')
        self.input.grid(row=2, column=1, sticky="ew")

        # Result below
        result_entry = ttk.Entry(head_frame, textvariable=self.result,
                                state='readonly', width=30, font=('Consolas', 8, 'normal'), justify='right')
        result_entry.grid(row=2, column=2,  sticky="we")

        for i, row in enumerate (currency_buttons):
            for j, col in enumerate(row):
                if col == 'USD':
                    btn = ttk.Button(keyboard_frame, text=col, command=self.to_usd)
                elif col == 'RUB':
                    btn = ttk.Button(keyboard_frame, text=col, command=self.to_rub)
                elif col == 'CNY':
                    btn = ttk.Button(keyboard_frame, text=col, command=self.to_cny)
                elif col == 'C':
                    btn = ttk.Button(keyboard_frame, text=col, command=self.clear)
                elif col == '⌫':
                    btn = ttk.Button(keyboard_frame, text=col, command=self.backspace)
                else:
                    btn = ttk.Button(keyboard_frame, text=col,
                                     command=lambda t=col: self.input_summa(t))
                btn.grid(row=i, column=j, sticky="we")

    def input_summa(self, text):
        curr = self.currency.get()
        if text == "USD":
            self.currency.set(curr+"USD")
        elif text == "RUB":
            self.currency.set(curr+"RUB")
        elif text == "CNY":
            self.currency.set(curr+"CNY")
        else:
            self.currency.set(curr + text)
        self.result.set("")

    def backspace(self):
        curr = self.currency.get()
        self.currency.set(curr[:-1])
        self.result.set("")
        
    def clear(self):
        self.currency.set("")
        self.result.set("")

    def to_usd(self):
        try:
            usd_crs = float(self.usd_courses.get())
            curr = float(self.currency.get())
            conv_usd = curr * usd_crs
            self.result.set(f"{conv_usd}")
        except ValueError:
            self.result.set("")
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число")
        except Exception as e:
            self.result.set("")
            messagebox.showerror("Ошибка", str(e))

    def to_rub(self):
        try:
            rub_crs = float(self.rub_courses.get())
            curr = float(self.currency.get())
            conv_rub = curr * rub_crs
            self.result.set(f"{conv_rub}")
        except ValueError:
            self.result.set("")
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число")
        except Exception as e:
            self.result.set("")
            messagebox.showerror("Ошибка", str(e))

    def to_cny(self):
        try:
            cny_crs = float(self.cny_courses.get())
            curr = float(self.currency.get())
            conv_cny = curr * cny_crs
            self.result.set(f"{conv_cny}")
        except ValueError:
            self.result.set("")
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число")
        except Exception as e:
            self.result.set("")
            messagebox.showerror("Ошибка", str(e))

    

        




if __name__ == "__main__":
    app = CurrencyConverter()
    app.window.mainloop()
    
