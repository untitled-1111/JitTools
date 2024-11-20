"""

     ▄█  ▄█      ███                                    
    ███ ███  ▀█████████▄                                
    ███ ███▌    ▀███▀▀██                                
    ███ ███▌     ███   ▀                                
    ███ ███▌     ███                                    
    ███ ███      ███                                    
    ███ ███      ███                                    
█▄ ▄███ █▀      ▄████▀                                  
▀▀▀▀▀▀                                                  
    ███      ▄██████▄   ▄██████▄   ▄█          ▄████████
▀█████████▄ ███    ███ ███    ███ ███         ███    ███
   ▀███▀▀██ ███    ███ ███    ███ ███         ███    █▀ 
    ███   ▀ ███    ███ ███    ███ ███         ███       
    ███     ███    ███ ███    ███ ███       ▀███████████
    ███     ███    ███ ███    ███ ███                ███
    ███     ███    ███ ███    ███ ███▌    ▄    ▄█    ███
   ▄████▀    ▀██████▀   ▀██████▀  █████▄▄██  ▄████████▀ 
                                  ▀                    

    GitHub: https://github.com/untitled-1111/JitTools
    License: MIT

"""

try:
    import os
    import sys
    import ctypes
    import tkinter as tk
    from requests import get
    import customtkinter
    
    import modules.LJD_Decompiler
    import modules.unprot
    import modules.debug
    import modules.deobf
    import modules.LJD_Compiler
    import modules.instruct

    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("icon/theme.json")  # Themes: "blue" (standard), "dark-blue", "green"

    internet_available = False
    version = os.path.splitext(os.path.basename(sys.argv[0]))[0].split("v")[1].split()[0]

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width - 700) // 2
            y = (screen_height - 380) // 2 + 20

            self.geometry(f"700x380+{x}+{y}")

            # configure window
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")
            else:
                self.title(f"JitTools v{version}")

            customtkinter.set_widget_scaling(1.1)  # текст мелкий пиздец, нихуя не видно
            self.iconbitmap("icon/icon.ico")

            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)

            self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text=f"JitTools GUI", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn1_event, text="Декомпиляция")
            self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=7)

            self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn2_event, text="Деобфускация")
            self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=7)

            self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn3_event, text="Анализ кода")
            self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=7)

            self.sidebar_button_1.invoke()

        def btn1_event(self):
            self.tabview = customtkinter.CTkTabview(self, width=500)
            self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")
            
            # Add tabs and configure them
            self.tabview.add("Декомпилятор")
            self.tabview.add("Анпротектор")
            
            for tab in ["Декомпилятор", "Анпротектор"]:
                self.tabview.tab(tab).grid_columnconfigure(0, weight=1)

            # Configure Decompiler tab
            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Декомпилятор"), dynamic_resizing=True,
                                                             values=["LuaJIT Fork", "Python Fork"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Декомпилятор"), 
                                                          command=lambda: self.decompile_event(self.optionmenu_1.get()), 
                                                          text="Запустить", width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=(2))

            # Configure Unprotection tab
            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Анпротектор"), dynamic_resizing=True,
                                                             values=["Unprot v2.1"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Анпротектор"), 
                                                          command=lambda: self.unprot_event(self.optionmenu_2.get()), 
                                                          text="Запустить", width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=(2))

        def decompile_event(self,_):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tk.tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

            if self.optionmenu_1.get() == "LuaJIT Fork":
                modules.LJD_Decompiler.ljd_Decompiler(file_path)

            elif self.optionmenu_1.get() == "Python Fork":
                modules.LJD_Decompiler.py_Decompiler(file_path)

        def unprot_event(self, _):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

            if self.optionmenu_2.get() == "Unprot v2.1":
                modules.unprot.unprot_2(file_path)

            
        def btn2_event(self):
            self.tabview = customtkinter.CTkTabview(self, width=500)
            self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

            self.tabview.add("Запуск кода")
            self.tabview.add("Деобфускация")

            self.tabview.tab("Запуск кода").grid_columnconfigure(0, weight=1)
            self.tabview.tab("Деобфускация").grid_columnconfigure(0, weight=1)

            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Запуск кода"), dynamic_resizing=True,
                                                            values=["Moonsec Dump", "Hook Obf", "Debugger", "XOR Unpack"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Запуск кода"), command=lambda: self.debug_event(self.optionmenu_1.get()), text="Запустить", width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)


            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Деобфускация"), dynamic_resizing=True,
                                                            values=["Base64 Deobf", "Shit Deobf"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Деобфускация"), command=lambda: self.deobf_event(self.optionmenu_1.get()), text="Запустить", width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)

        def btn3_event(self):
            self.tabview = customtkinter.CTkTabview(self, width=500)
            self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

            self.tabview.add("Компиляция")
            self.tabview.add("Просмотр инструкций")

            self.tabview.tab("Компиляция").grid_columnconfigure(0, weight=1)
            self.tabview.tab("Просмотр инструкций").grid_columnconfigure(0, weight=1)

            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Компиляция"), dynamic_resizing=True,
                                                            values=["LuaJIT Compiler", "Joiner"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Компиляция"), command=lambda: self.compile_event(self.optionmenu_1.get()), text="Запустить", width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)

            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Просмотр инструкций"), dynamic_resizing=True,
                                                            values=["Luad", "BCViewer", "ASM"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Просмотр инструкций"), command=lambda: self.instruct_event(self.optionmenu_1.get()), text="Запустить", width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)

        def debug_event(self, _):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

            if self.optionmenu_1.get() == "Moonsec Dump":
                modules.debug.moonsecdump(file_path)

            elif self.optionmenu_1.get() == "Hook Obf":
                modules.debug.hookobf(file_path)

            elif self.optionmenu_1.get() == "Debugger":
                modules.debug.debugger(file_path)

            elif self.optionmenu_1.get() == "XOR Unpack":
                modules.debug.xorunpack(file_path)

        def deobf_event(self, _):
            if self.optionmenu_2.get() == "Base64 Deobf":
                input = tk.simpledialog.askstring("Base64 Deobf", "Введите зашифрованный код, и результат будет сохранен в файле: Decode - JTools (B64).txt: ")
                if len(input) < 1:
                    tk.messagebox.showinfo("Base64 Deobf", "Вы ничего не ввели.")
                else:
                    modules.deobf.base64d(input)

            elif self.optionmenu_2.get() == "Shit Deobf":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")
                modules.deobf.shitd(file_path)

        def compile_event(self, _):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

            if self.optionmenu_1.get() == "LuaJIT Compiler":
                modules.LJD_Compiler.compiler(file_path)

            elif self.optionmenu_1.get() == "Joiner":
                modules.LJD_Compiler.joiner(file_path)


        def instruct_event(self, _):
            if self.optionmenu_2.get() == "BCViewer":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")
                modules.instruct.bcviewer(file_path)

            elif self.optionmenu_2.get() == "Luad":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")


                file_path = sys.argv[1]
                base, ext = os.path.splitext(file_path)

                if ext != ".luac" and os.path.isfile(file_path):
                    new_file_path = base + '.luac'
                    os.rename(file_path, new_file_path)

                modules.instruct.luad()

            elif self.optionmenu_2.get() == "ASM":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tk.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")
                modules.instruct.asm(file_path)


    if __name__ == "__main__":
        # консоль в центре
        class RECT(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

        ctypes.windll.user32.SetProcessDPIAware()
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        cx = width // 2
        cy = height // 2
        x = (ctypes.windll.user32.GetSystemMetrics(0) - width) // 2
        y = (ctypes.windll.user32.GetSystemMetrics(1) - height) // 2
        ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, 0)
        ctypes.windll.user32.ShowWindow(hwnd, 2)  # SW_MINIMIZE

        root = tk.Tk()

        # проверка наличия интернета и новой версии (авто-обновления нету)
        try:
            response = get("https://raw.githubusercontent.com/untitled-1111/JitTools/refs/heads/master/check_update", stream=True)
            response.raise_for_status()
            response_lines = response.iter_lines(decode_unicode=True)
            new_version = next(response_lines).strip()
            log = "\n".join(response_lines)

            if float(new_version) > float(version):
                root.withdraw()
                response = tk.messagebox.askyesno(
                    "Доступно обновление",
                    f"Доступна новая версия JitTools v{new_version}\n\n{log}\n\nОткрыть страницу загрузки?"
                )
                if response:
                    from webbrowser import open
                    open("https://github.com/untitled-1111/JitTools/releases")
                    sys.exit()

        except OSError: # если интернет отсутствует
            pass

        root.destroy()
        app = App()
        app.mainloop()

except Exception as e:
    from pyperclip import copy
    tk.messagebox.showinfo("Ошибка JitTools", f"Произошла ошибка, отладочная информация скопирована в буфер обмена, отправьте ее разработчику!")
    
    if len(sys.argv) > 1:
        debug_text = f"JitTools v{version} | ERROR: [{e.__traceback__.tb_lineno}] {e} | FILENAME: {os.path.basename(sys.argv[1])}"
    else:
        debug_text = f"JitTools v{version} | ERROR: [{e.__traceback__.tb_lineno}] {e} | FILENAME: None"
        
    copy(debug_text)

    ctypes.windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL
    sys.exit()