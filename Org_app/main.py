import customtkinter as ctk
import psycopg2
from tkinter import messagebox

# Конфигурация темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ВАЖНО: Убедитесь, что параметры подключения верны для вашей текущей базы
DB_CONFIG = {
    "dbname": "master_services_db", 
    "user": "postgres",
    "password": "aasl8998",
    "host": "localhost",
    "port": "5432"
}

class ServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Service Master Pro")
        self.geometry("600x750")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Интерфейс
        self.label_title = ctk.CTkLabel(self, text="Учет услуг компании", font=("Segoe UI", 24, "bold"))
        self.label_title.grid(row=0, column=0, pady=20)

        self.main_tab = ctk.CTkTabview(self, height=250)
        self.main_tab.grid(row=1, column=0, padx=20, sticky="nsew")

        self.main_tab.add("Калькулятор")
        self.main_tab.add("Услуги")
        self.main_tab.add("Управление")

        self.setup_calc_tab()
        self.setup_services_tab()
        self.setup_admin_tab()

        self.report_frame = ctk.CTkScrollableFrame(self, label_text="Последние расчеты", label_font=("Segoe UI", 14, "bold"))
        self.report_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # ПРИНУДИТЕЛЬНЫЙ ЗАПУСК ОБНОВЛЕНИЯ ПРИ СТАРТЕ
        self.refresh_all_data()

    def setup_calc_tab(self):
        tab = self.main_tab.tab("Калькулятор")
        tab.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab, text="Выберите услугу:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.option_menu = ctk.CTkOptionMenu(tab, values=["Загрузка..."])
        self.option_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(tab, text="Кол-во (часы/ед):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantity = ctk.CTkEntry(tab, placeholder_text="1")
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.btn_calc = ctk.CTkButton(tab, text="Рассчитать и сохранить", command=self.calculate)
        self.btn_calc.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        self.label_result = ctk.CTkLabel(tab, text="Итого: 0 смн.", font=("Arial", 16, "bold"), text_color="#3b8ed0")
        self.label_result.grid(row=3, column=0, columnspan=2, pady=5)

    def setup_services_tab(self):
        tab = self.main_tab.tab("Услуги")
        tab.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(tab, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_name = ctk.CTkEntry(tab)
        self.input_name.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(tab, text="Цена:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.input_price = ctk.CTkEntry(tab)
        self.input_price.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(tab, text="Добавить тип услуги", fg_color="#28a745", command=self.create_service_type).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def setup_admin_tab(self):
        tab = self.main_tab.tab("Управление")
        ctk.CTkButton(tab, text="Обновить все данные", command=self.refresh_all_data).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(tab, text="Выход", command=self.destroy, fg_color="#dc3545").pack(pady=10, fill="x", padx=20)

    # --- ИСПРАВЛЕННАЯ ЛОГИКА ---

    def refresh_all_data(self):
        """Полное обновление интерфейса"""
        self.refresh_menu()
        self.get_services_calculation()

    def refresh_menu(self):
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                # Используем обычный курсор, так как столбцы теперь именованные
                with conn.cursor() as cur:
                    # ВАЖНО: используем SELECT * FROM
                    cur.execute("SELECT name, price FROM masters_services.get_services_price();")
                    rows = cur.fetchall()
                    
                    services = [row[0] for row in rows] # row[0] это 'name', row[1] это 'price'
                    
                    if services:
                        self.option_menu.configure(values=services)
                        self.option_menu.set(services[0])
        except Exception as e:
            print(f"Ошибка: {e}")

    def calculate(self):
        try:
            # 1. Получаем данные из интерфейса
            service = self.option_menu.get()
            qty_text = self.entry_quantity.get().strip().replace(',', '.')
            
            if not qty_text:
                messagebox.showwarning("Внимание", "Введите количество")
                return
                
            qty = float(qty_text)

            # 2. Подключаемся к базе
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    # Вызываем функцию через SELECT * FROM, как мы договорились
                    cur.execute("SELECT name, price FROM masters_services.get_services_price()")
                    prices_data = cur.fetchall()
                    
                    price = 0
                    found = False

                    # 3. Ищем цену выбранной услуги в полученных данных
                    for row in prices_data:
                        print(row[0], row[1])
                        # row[0] - это name, row[1] - это price
                        if row[0] == service:
                            price = float(row[1])
                            found = True
                            break
                    
                    if found:
                        total = qty * price
                        self.label_result.configure(text=f"Итого: {total:.2f} смн.")
                        
                        # 4. Сохраняем расчет в базу данных
                        # Используем явное приведение типов для стабильности в Neon/Postgres
                        cur.execute(
                            "CALL masters_services.create_calculation(%s::varchar, %s::numeric, %s::numeric)", 
                            (service, qty, total)
                        )
                        conn.commit()
                    else:
                        messagebox.showwarning("Ошибка", "Цена для выбранной услуги не найдена в базе.")
                        return

            # 5. Обновляем визуальный отчет снизу
            self.get_services_calculation()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом (например: 5 или 1.5)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось рассчитать: {e}")

    def get_services_calculation(self):
        """Очистка и обновление отчета"""
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM masters_services.get_services();")
                    for index, row in enumerate(cur.fetchall()):
                        text = f"Название: {row[0]} | Кол-во: {row[1]} | Сумма: {row[2]} смн. | Дата: {row[3]} "
                        ctk.CTkLabel(self.report_frame, text=text, font=("Consolas", 11), anchor="w").grid(row=index, column=0, sticky="ew", padx=10, pady=2)
        except Exception as e:
            print(f"Ошибка отчета: {e}")

    def create_service_type(self):
        name = self.input_name.get().strip()
        price = self.input_price.get().strip()
        if not name or not price: return

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL masters_services.create_service_type(%s::varchar, %s::numeric)", (name, price))
                    conn.commit()
            messagebox.showinfo("Успех", f"Услуга '{name}' добавлена")
            self.refresh_menu()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    app = ServiceApp()
    app.mainloop()