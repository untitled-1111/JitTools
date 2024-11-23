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
    import customtkinter
    import tkinter
    import configparser
    
    import modules.decompiler
    import modules.unprot
    import modules.debug
    import modules.deobf
    import modules.compiler
    import modules.instruct

    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("gui/theme.json")  # Themes: "blue" (standard), "dark-blue", "green"

    internet_available = False
    version = os.path.splitext(os.path.basename(sys.argv[0]))[0].split("v")[1].split()[0]

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()

            # configure window
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width - 700) // 2
            y = (screen_height - 380) // 2 + 20

            self.geometry(f"700x380+{x}+{y}")
            customtkinter.set_widget_scaling(1.1)  # текст мелкий пиздец, нихуя не видно

            self.iconbitmap("gui/icon.ico")
            
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

                # decompiler
                if config['Checkbox'].getint('decompiler_luajit_fork') == 1:
                    result = tkinter.messagebox.askyesno("Декомпиляция", "Применить декомпилятор LuaJIT Fork?")
                    if result:
                        modules.decompiler.ljd_decompiler(file_path)

                elif config['Checkbox'].getint('decompiler_python_fork') == 1:
                    result = tkinter.messagebox.askyesno("Декомпиляция", "Применить декомпилятор Python Fork?")
                    if result:
                        modules.decompiler.py_decompiler(file_path)
                    
            else:
                self.title(f"JitTools v{version}")

            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)

            self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="JitTools GUI", font=customtkinter.CTkFont(size=20, weight="bold"))
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
            
            self.tabview.add("Декомпилятор")
            self.tabview.add("Анпротектор")
            
            for tab in ["Декомпилятор", "Анпротектор"]:
                self.tabview.tab(tab).grid_columnconfigure(0, weight=1)


            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Декомпилятор"), command=self.combo_event, dynamic_resizing=True,\
                                                             values=["LuaJIT Fork", "Python Fork"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Декомпилятор"), 
                                                          command=lambda: self.decompile_event(self.optionmenu_1.get()), 
                                                          text="Запустить", width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=(2))

            self.checkbox_1 = customtkinter.CTkCheckBox(self.tabview.tab("Декомпилятор"), command=lambda: self.checkbox_event(self.optionmenu_1.get()), text="Применять ко всем скриптам")
            self.checkbox_1.grid(row=2, column=0, padx=20, pady=(8))


            config.read('JitTools.ini')
            checkbox_key = f'decompiler_{self.optionmenu_1.get().lower().replace(" ", "_")}'

            if checkbox_key in config['Checkbox']:
                is_checked = config['Checkbox'].getboolean(checkbox_key)
            else:
                is_checked = False

            self.checkbox_1.select() if is_checked else self.checkbox_1.deselect()


            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Анпротектор"), dynamic_resizing=True,
                                                             values=["Unprot v2.1"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Анпротектор"), 
                                                          command=lambda: self.unprot_event(self.optionmenu_2.get()), 
                                                          text="Запустить", width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=(2))


        def checkbox_event(self, _):
            config.read('JitTools.ini')
            config.set('Checkbox', f'decompiler_{self.optionmenu_1.get().lower().replace(" ", "_")}', str(self.checkbox_1.get()))
            with open('JitTools.ini', 'w') as configfile:
                config.write(configfile)

            if not 'decompiler_luajit_fork' in config['Checkbox'] or not 'decompiler_python_fork' in config['Checkbox']:
                tkinter.messagebox.showinfo("JitTools", "Данная функция будет работать на все скрипты, перемещенные при помощи Drag&Drop, или указанные в аргумент командной строки.")

        def combo_event(self, _):
            config.read('JitTools.ini')
            checkbox_key = f'decompiler_{self.optionmenu_1.get().lower().replace(" ", "_")}'

            if checkbox_key in config['Checkbox']:
                is_checked = config['Checkbox'].getboolean(checkbox_key)
            else:
                is_checked = False

            self.checkbox_1.select() if is_checked else self.checkbox_1.deselect()

        def decompile_event(self,_):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

            if self.optionmenu_1.get() == "LuaJIT Fork":
                modules.decompiler.ljd_decompiler(file_path)

            elif self.optionmenu_1.get() == "Python Fork":
                modules.decompiler.py_decompiler(file_path)

        def unprot_event(self, _):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
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
                file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
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
                input = tkinter.simpledialog.askstring("B64", "Введите зашифрованный код: ")
                if len(input) < 1:
                    tkinter.messagebox.showinfo("B64", "Вы ничего не ввели.")
                else:
                    modules.deobf.base64d(input)
                    tkinter.messagebox.showinfo("Base64 Deobf", "Успешно сохранено в файл Decode - JitTools (B64).txt")

            elif self.optionmenu_2.get() == "Shit Deobf":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")
                modules.deobf.shitd(file_path)

        def compile_event(self, _):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.basename(file_path)}")

            if self.optionmenu_1.get() == "LuaJIT Compiler":
                modules.compiler.compiler(file_path)

            elif self.optionmenu_1.get() == "Joiner":
                modules.compiler.joiner(file_path)


        def instruct_event(self, _):
            if self.optionmenu_2.get() == "BCViewer":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.basename(file_path)}")
                modules.instruct.bcviewer(file_path)

            elif self.optionmenu_2.get() == "Luad":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
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
                    file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
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

        root = tkinter.Tk()
        config = configparser.ConfigParser()

        # проверка наличия интернета и новой версии (авто-обновления нету)
        try:
            from requests import get
            response = get("https://raw.githubusercontent.com/untitled-1111/JitTools/refs/heads/master/check_update", stream=True)
            response.raise_for_status()
            response_lines = response.iter_lines(decode_unicode=True)
            new_version = next(response_lines).strip()
            log = "\n".join(response_lines)

            if float(new_version) > float(version):
                root.withdraw()
                response = tkinter.messagebox.askyesno(
                    "Доступно обновление",
                    f"Доступна новая версия JitTools v{new_version}\n\n{log}\n\nОткрыть страницу загрузки?"
                )
                if response:
                    from webbrowser import open
                    open("https://github.com/untitled-1111/JitTools/releases")
                    sys.exit()

        except OSError: # если интернет отсутствует
            pass

        if not os.path.exists('JitTools.ini'):
            with open('JitTools.ini', 'w') as f:
                f.close()

        if not config.has_section('Checkbox'):
            config.add_section('Checkbox')

        root.destroy()
        app = App()
        app.mainloop()

except Exception as e:
    if len(sys.argv) > 1:
        debug_text = f"JitTools v{version} | ERROR: [{e.__traceback__.tb_lineno}] {e} | FILENAME: {os.path.basename(sys.argv[1])}"
    else:
        debug_text = f"JitTools v{version} | ERROR: [{e.__traceback__.tb_lineno}] {e} | FILENAME: None"
        
    from pyperclip import copy
    copy(debug_text)

    tkinter.messagebox.showinfo("Ошибка JitTools", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e} \n\nОтладочная информация скопирована в буфер обмена, отправьте ее разработчику!")
    ctypes.windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL
    sys.exit()