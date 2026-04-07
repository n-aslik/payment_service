# import customtkinter as ctk
# import psycopg2
# from tkinter import messagebox

# # Конфигурация подключения к базе данных
# # ЗАМЕНИ ЭТИ ДАННЫЕ НА СВОИ
# DB_CONFIG = {
#     "dbname": "master_services_db" ,
#     "user": "postgres",
#     "password": "aasl8998",
#     "host": "localhost",
#     "port": "5432"
# }

# class ServiceApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("Калькулятор услуг компании")
#         self.geometry("450x455")
#         self.resizable(True, True)

#         # Панель
                     
#         main_tab = ctk.CTkTabview(self,segmented_button_selected_color="blue", height=140, width=40)
#         main_tab.grid(row = 0, column = 0, sticky = "nsew", rowspan = 5, padx = 8, pady = 5)

#         main_tab.add("Выход")
#         main_tab.add("Услуги")
#         main_tab.add("Отчёт")

#         tabbtn1 = ctk.CTkButton(main_tab.tab("Выход"), text="Выйти", command=self.close_app)
#         tabbtn1.grid(row = 0, column = 0 , padx = 10)

#         lable_name = ctk.CTkLabel(main_tab.tab("Услуги"), text="Услуга")
#         lable_name.grid(row = 0, column = 0, sticky = "nsew")

#         lable_price = ctk.CTkLabel(main_tab.tab("Услуги"), text="Цена")
#         lable_price.grid(row = 1, column = 0, sticky = "nsew")

#         self.input_name = ctk.CTkEntry(main_tab.tab("Услуги"))
#         self.input_name.grid(row = 0, column = 1, sticky = "nsew", padx= 5)

#         self.input_price = ctk.CTkEntry(main_tab.tab("Услуги"))
#         self.input_price.grid(row = 1, column = 1, sticky = "nsew", padx= 5)

#         tabbtn2 = ctk.CTkButton(main_tab.tab("Услуги"), text="Добавить", command=self.create_service_type)
#         tabbtn2.grid(row = 2, column = 0, columnspan= 2, sticky ="nsew", pady = 2)

#         tabbtn3 = ctk.CTkButton(main_tab.tab("Отчёт"), text="Показать", command=self.get_services_calculation)
#         tabbtn3.grid(row = 0, column = 0, padx = 10,  sticky ="nsew")

#         # Настройка интерфейса
#         self.label_title = ctk.CTkLabel(self, text="Расчет стоимости", font=("Arial", 20, "bold"))
#         self.label_title.grid(row = 0, column = 1, sticky = "nsew", padx = 5, pady = 5)

#         result = self.get_services()
    
#         services_names = [i["name"] for i in result]
#         # Выбор услуги
#         if services_names:
#             self.service_var = ctk.StringVar(value=services_names[0])
        
#             self.option_menu = ctk.CTkOptionMenu(self, values=services_names, variable=self.service_var)

#         self.option_menu.grid(row = 2, column = 1, sticky = "nsew", padx = 5, pady = 5)

#         # Поле ввода количества (например, часов)
#         self.entry_quantity = ctk.CTkEntry(self, placeholder_text="Введите количество часов")
#         self.entry_quantity.grid(row = 3, column = 1, sticky = "nsew", padx = 5, pady = 5)

#         # Кнопка расчета
#         self.btn_calc = ctk.CTkButton(self, text="Рассчитать и сохранить", command=self.calculate)
#         self.btn_calc.grid(row = 4, column = 1, sticky = "nsew", padx = 5, pady = 5)

#         # Вывод результата
#         self.label_result = ctk.CTkLabel(self, text="Итого: 0 смн.", font=("Arial", 16))
#         self.label_result.grid(row = 5, column = 0, columnspan=2, sticky = "nsew", padx = 5, pady = 5)

#         self.report_frame = ctk.CTkScrollableFrame(self, width=410, label_text="Отчёт", orientation="vertical")
#         self.report_frame.grid(row = 6, column = 0, columnspan= 2, sticky = "nsew", padx = 10, pady = 5)
    
#     def refresh_menu(self):
#     # 1. Получаем обновленные данные (например, заново вызываем ваш запрос к БД)
#         result = self.get_services() 
    
#     # 2. Формируем новый список названий
#         new_names = [i["name"] for i in result]
    
#     # 3. ОБНОВЛЯЕМ виджет через configure
#         self.option_menu.configure(values=new_names)
    
#     # 4. Опционально: сбрасываем выбранное значение на первое из списка
#         if new_names:
#             self.service_var.set(new_names[0])

#     def refresh_report(self):
#     # 1. Получаем обновленные данные (например, заново вызываем ваш запрос к БД)
#         result = self.get_services_calculation 
    
#     # 2. Формируем новый список названий
#         new_names = [i for i in result]
    
#     # 3. ОБНОВЛЯЕМ виджет через configure
#         self.report.configure(values=new_names)
    
#     def close_app(self):
#         self.quit()

#     def get_services(self):
#         try:
#             conn = psycopg2.connect(**DB_CONFIG)
#             cur = conn.cursor()
#             cur.execute(
#                 "SELECT masters_services.get_services_price()")
#             result = cur.fetchone()[0]
#             return result
#         except Exception as e:
#             messagebox.showerror("Ошибка БД", f"Не удалось найти: {e}")

#     def get_services_calculation(self):
#         conn = None
#         try:
#             conn = psycopg2.connect(**DB_CONFIG)
#             cur = conn.cursor()
            
#             # Вызываем функцию
#             cur.execute("SELECT * FROM masters_services.get_services();")
#             result = cur.fetchall()
            
#             start_row = 0
            
#             for index, row in enumerate(result):
#                 text_value = " | ".join(str(val) for val in row) 
                
#                 self.report = ctk.CTkLabel(self.report_frame, text=text_value)
#                 self.report.grid(row=start_row + index, column=0, sticky="w", columnspan=2, padx=10, pady=2)
            
                
#         except Exception as e:
#             messagebox.showerror("Ошибка БД", f"Произошла ошибка: {e}")
#         finally:
#             # Обязательно закрываем соединение
#             if conn:
#                 cur.close()
#                 conn.close()

#     def calculate(self):
#         conn = None
#         try:
#             # 1. Получаем и очищаем ввод
#             selected_service_name = self.service_var.get()
#             raw_quantity = self.entry_quantity.get().strip()
            
#             # Проверка на пустоту
#             if not raw_quantity:
#                 messagebox.showwarning("Внимание", "Введите количество часов")
#                 return

#             # Преобразование (здесь может быть ValueError №1)
#             quantity = float(raw_quantity.replace(',', '.'))

#             # 2. Работа с БД
#             conn = psycopg2.connect(**DB_CONFIG)
#             cur = conn.cursor()
            
#             cur.execute("SELECT * FROM masters_services.get_services_price()")
#             prices = cur.fetchall()

#             total = 0
#             found = False

#             for row in prices:
#                 # В PostgreSQL результат fetchall() — это список кортежей.
#                 # Если функция возвращает JSON/Record, данные лежат в row[0]
#                 data = row[0] 

#                 # Проверяем, что data — это действительно словарь
#                 if isinstance(data, dict):
#                     service_name_db = str(data.get("name", "")).strip()
#                     service_price_db = data.get("price", 0)
                    
#                     if service_name_db == selected_service_name.strip():
#                         total = quantity * float(service_price_db)
#                         found = True
#                         break
            
#             if found:
#                 self.label_result.configure(text=f"Итого: {total} смн.")
#                 # Вызываем сохранение
#                 self.save_to_db(selected_service_name, quantity, total)
#             else:
#                 messagebox.showwarning("Внимание", "Выбранная услуга не найдена")

#         except ValueError as ve:
#             # Выводим конкретную ошибку в консоль для отладки
#             print(f"Ошибка значения: {ve}")
#             messagebox.showerror("Ошибка", f"Некорректные данные: {ve}\nПроверьте ввод количества.")
#         except Exception as e:
#             print(f"Общая ошибка: {e}")
#             messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
#         finally:
#             if conn:
#                 cur.close()
#                 conn.close()

#     def create_service_type(self):
#         try:
#             name = self.input_name.get()
#             price = self.input_price.get()

#             self.save_service_type(name, price)

#         except ValueError:
#             messagebox.showerror("Ошибка", "Пожалуйста, введите текстовое значение" )
        
#     def save_service_type(self, serv, price):
#         try:
#             conn = psycopg2.connect(**DB_CONFIG)
#             cur = conn.cursor()
#             cur.execute(
#                 "CALL masters_services.create_service_type(%s, %s)",
#                 (serv, price)
#             )
#             conn.commit()
#             cur.close()
#             conn.close()
#             messagebox.showinfo("Инфо", "Данные успешно сохранены!")
#             self.refresh_menu()
#         except Exception as e:
#             messagebox.showerror("Ошибка БД", f"Не удалось сохранить: {e}")

#     def save_to_db(self, service, qty, total):
#         try:
#             conn = psycopg2.connect(**DB_CONFIG)
#             cur = conn.cursor()
#             cur.execute(
#                 "CALL masters_services.create_calculation(%s, %s, %s)",
#                 (service, qty, total)
#             )
#             conn.commit()
#             cur.close()
#             conn.close()
#             messagebox.showinfo("Инфо", "Данные успешно сохранены!")
#             self.refresh_report

#         except Exception as e:
#             messagebox.showerror("Ошибка БД", f"Не удалось сохранить: {e}")

# if __name__ == "__main__":
#     app = ServiceApp()
#     app.mainloop()
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