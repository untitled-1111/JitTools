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
    import customtkinter
    import tkinter
    
    from configparser import ConfigParser
    from webbrowser import open as open_browser
    from ctypes import windll, byref, Structure, c_long
    
    import modules.decompiler
    import modules.unprot
    import modules.debug
    import modules.deobf
    import modules.compiler
    import modules.instruct

    config = ConfigParser()
    if not os.path.exists('JitTools.ini'):
        with open('JitTools.ini', 'w') as f:
            f.close()

    if not config.has_section('Checkbox'):
        config.add_section('Checkbox')

    if not config.has_section('Main'):
        config.add_section('Main')

    config.read('JitTools.ini')
    theme = config['Main'].get('theme')
    if theme not in ('Dark', 'Light', 'System'):
        theme = 'System'
        config['Main']['theme'] = theme

    if theme != customtkinter.get_appearance_mode:
        customtkinter.set_appearance_mode(theme)
        if theme == 'Light':
            customtkinter.set_default_color_theme("gui/theme_light.json")
        else:
            customtkinter.set_default_color_theme("gui/theme.json")

    with open('JitTools.ini', 'w') as f:
        config.write(f)

    internet_available = False
    version = os.path.splitext(os.path.basename(sys.argv[0]))[0].split("v")[1]

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
            
            if len(sys.argv) > 1 and os.path.splitext(sys.argv[1])[1].lower() in ['.lua', '.luac', '.txt']:
                file_path = sys.argv[1]
                self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")
               
                # decompiler
                if config['Checkbox'].getint('decompiler_luajit_fork') == 1:
                    result = tkinter.messagebox.askyesno(lang["decompilation"], f"{lang['apply_decompiler']} LuaJIT Fork?")
                    if result:
                        modules.decompiler.ljd_decompiler(file_path)

                elif config['Checkbox'].getint('decompiler_python_fork') == 1:
                    result = tkinter.messagebox.askyesno(lang["decompilation"], f"{lang['apply_decompiler']} Python Fork?")
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

            self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn1_event, text=lang["decompilation"])
            self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=7)

            self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn2_event, text=lang["deobfuscation"])
            self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=7)

            self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn3_event, text=lang["code_analysis"])
            self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=7)

            self.sidebar_button_1.invoke()

        def btn1_event(self):
            self.sidebar_button_1.configure(border_color="#77858f", border_width=2)
            self.sidebar_button_2.configure(border_color="#3E454A", border_width=0)
            self.sidebar_button_3.configure(border_color="#3E454A", border_width=0)

            self.tabview = customtkinter.CTkTabview(self, width=500)
            self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")
            
            self.tabview.add(lang["decompiler"])
            self.tabview.add(lang["unprotector"])
            
            for tab in [lang["decompiler"], lang["unprotector"]]:
                self.tabview.tab(tab).grid_columnconfigure(0, weight=1)


            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["decompiler"]), command=self.combo_event, dynamic_resizing=True,\
                                                             values=["LuaJIT Fork", "Python Fork"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab(lang["decompiler"]), 
                                                          command=lambda: self.decompile_event(), 
                                                          text=lang["start"], width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=(2))

            self.checkbox_1 = customtkinter.CTkCheckBox(self.tabview.tab(lang["decompiler"]), command=lambda: self.checkbox_event(), text=lang["checkbox_name"])
            self.checkbox_1.grid(row=2, column=0, padx=20, pady=(12))


            config.read('JitTools.ini')
            checkbox_key = f'decompiler_{self.optionmenu_1.get().lower().replace(" ", "_")}'

            if checkbox_key in config['Checkbox']:
                is_checked = config['Checkbox'].getboolean(checkbox_key)
            else:
                is_checked = False

            self.checkbox_1.select() if is_checked else self.checkbox_1.deselect()


            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["unprotector"]), dynamic_resizing=True,
                                                             values=["Unprot v2.1"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab(lang["unprotector"]), 
                                                          command=lambda: self.unprot_event(), 
                                                          text=lang["start"], width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=(2))


        def checkbox_event(self):
            config.read('JitTools.ini')
            config.set('Checkbox', f'decompiler_{self.optionmenu_1.get().lower().replace(" ", "_")}', str(self.checkbox_1.get()))
            with open('JitTools.ini', 'w') as configfile:
                config.write(configfile)

            if not 'decompiler_luajit_fork' in config['Checkbox'] or not 'decompiler_python_fork' in config['Checkbox']:
                tkinter.messagebox.showinfo("JitTools", lang["checkbox_description"])

        def combo_event(self, _):
            config.read('JitTools.ini')
            checkbox_key = f'decompiler_{self.optionmenu_1.get().lower().replace(" ", "_")}'

            if checkbox_key in config['Checkbox']:
                is_checked = config['Checkbox'].getboolean(checkbox_key)
            else:
                is_checked = False

            self.checkbox_1.select() if is_checked else self.checkbox_1.deselect()

        def decompile_event(self):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")

            if self.optionmenu_1.get() == "LuaJIT Fork":
                modules.decompiler.ljd_decompiler(file_path)

            elif self.optionmenu_1.get() == "Python Fork":
                modules.decompiler.py_decompiler(file_path)

        def unprot_event(self):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")

            if self.optionmenu_2.get() == "Unprot v2.1":
                modules.unprot.unprot_2(file_path)

            
        def btn2_event(self):
            self.sidebar_button_2.configure(border_color="#77858f", border_width=2)
            self.sidebar_button_1.configure(border_color="#3E454A", border_width=0)
            self.sidebar_button_3.configure(border_color="#3E454A", border_width=0)

            self.tabview = customtkinter.CTkTabview(self, width=500)
            self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

            self.tabview.add(lang["running_code"])
            self.tabview.add(lang["deobfuscation"])

            for tab in [lang["running_code"], lang["deobfuscation"]]:
                self.tabview.tab(tab).grid_columnconfigure(0, weight=1)

            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["running_code"]), dynamic_resizing=True,
                                                            values=["Moonsec Dump", "Hook Obf", "Debugger", "XOR Unpack"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab(lang["running_code"]), command=lambda: self.debug_event(), text=lang["start"], width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)


            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["deobfuscation"]), dynamic_resizing=True,
                                                            values=["Base64 Deobf", "Shit Deobf"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab(lang["deobfuscation"]), command=lambda: self.deobf_event(), text=lang["start"], width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)

        def btn3_event(self):
            self.sidebar_button_3.configure(border_color="#77858f", border_width=2)
            self.sidebar_button_1.configure(border_color="#3E454A", border_width=0)
            self.sidebar_button_2.configure(border_color="#3E454A", border_width=0)

            self.tabview = customtkinter.CTkTabview(self, width=500)
            self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

            self.tabview.add(lang["compilation"])
            self.tabview.add(lang["instructions"])
            self.tabview.add(lang["web_tools"])

            for tab in [lang["compilation"], lang["instructions"], lang["web_tools"]]:
                self.tabview.tab(tab).grid_columnconfigure(0, weight=1)

            self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["compilation"]), dynamic_resizing=True,
                                                            values=["LuaJIT Compiler", "Joiner"])
            self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab(lang["compilation"]), command=lambda: self.compile_event(), text=lang["start"], width=100)
            self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)


            self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["instructions"]), dynamic_resizing=True,
                                                            values=["Bytecode Editor", "Luad", "BCViewer", "ASM"])
            self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab(lang["instructions"]), command=lambda: self.instruct_event(), text=lang["start"], width=100)
            self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)


            self.optionmenu_3 = customtkinter.CTkOptionMenu(self.tabview.tab(lang["web_tools"]), dynamic_resizing=True,
                                                            values=["LuaJIT Scanner", "HexEd.it", "Lua Beautify", "Lua Online"])
            self.optionmenu_3.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.button_tab_3 = customtkinter.CTkButton(self.tabview.tab(lang["web_tools"]), command=lambda: self.web_event(), text=lang["open"], width=100)
            self.button_tab_3.grid(row=1, column=0, padx=20, pady=2)

        def web_event(self):
            links = {
                "LuaJIT Scanner": "https://luajit.ru/",
                "HexEd.it": "https://hexed.it/",
                "Lua Beautify": "https://codebeautify.org/lua-beautifier#",
                "Lua Online": "https://onecompiler.com/lua",
            }
            open_browser(links[self.optionmenu_3.get()])

        def debug_event(self):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")

            if self.optionmenu_1.get() == "Moonsec Dump":
                modules.debug.moonsecdump(file_path)

            elif self.optionmenu_1.get() == "Hook Obf":
                modules.debug.hookobf(file_path)

            elif self.optionmenu_1.get() == "Debugger":
                modules.debug.debugger(file_path)

            elif self.optionmenu_1.get() == "XOR Unpack":
                modules.debug.xorunpack(file_path)

        def deobf_event(self):
            if self.optionmenu_2.get() == "Base64 Deobf":
                input = tkinter.simpledialog.askstring("B64", f"{lang['enter_encrypted_code']}: ")
                if len(input) < 1:
                    tkinter.messagebox.showinfo("B64", lang["empty_input"])
                else:
                    modules.deobf.base64d(input)
                    tkinter.messagebox.showinfo("B64", f"{lang["saved_to_file"]}: Decode - JitTools (B64).txt")

            elif self.optionmenu_2.get() == "Shit Deobf":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")
                modules.deobf.shitd(file_path)

        def compile_event(self):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")

            if self.optionmenu_1.get() == "LuaJIT Compiler":
                modules.compiler.compiler(file_path)

            elif self.optionmenu_1.get() == "Joiner":
                modules.compiler.joiner(file_path)

        def instruct_event(self):
            if len(sys.argv) > 1:
                file_path = sys.argv[1]
            else:
                file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                if not file_path:
                    sys.exit()

            self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")

            if self.optionmenu_2.get() == "Bytecode Editor":
                modules.instruct.editor(file_path)

            elif self.optionmenu_2.get() == "BCViewer":
                modules.instruct.bcviewer(file_path)

            elif self.optionmenu_2.get() == "Luad":
                file_path = sys.argv[1]
                base, ext = os.path.splitext(file_path)

                if ext != ".luac" and os.path.isfile(file_path):
                    new_file_path = base + '.luac'
                    os.rename(file_path, new_file_path)

                modules.instruct.luad(file_path, ext)


            elif self.optionmenu_2.get() == "ASM":
                if len(sys.argv) > 1:
                    file_path = sys.argv[1]
                else:
                    file_path = tkinter.filedialog.askopenfilename(title=lang["select_file"], filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
                    if not file_path:
                        sys.exit()

                self.title(f"JitTools v{version} - {os.path.splitext(os.path.basename(file_path))[0][:27] + '..' if len(os.path.splitext(os.path.basename(file_path))[0]) > 27 else os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]}")
                modules.instruct.asm(file_path)


    if __name__ == "__main__":
        # консоль в центре
        class RECT(Structure):
            _fields_ = [("left", c_long), ("top", c_long), ("right", c_long), ("bottom", c_long)]

        windll.user32.SetProcessDPIAware()
        hwnd = windll.kernel32.GetConsoleWindow()
        rect = RECT()
        windll.user32.GetWindowRect(hwnd, byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        cx = width // 2
        cy = height // 2
        x = (windll.user32.GetSystemMetrics(0) - width) // 2
        y = (windll.user32.GetSystemMetrics(1) - height) // 2
        windll.user32.MoveWindow(hwnd, x, y, width, height, 0)
        windll.user32.ShowWindow(hwnd, 2)  # SW_MINIMIZE

        root = tkinter.Tk()
                    
        windll.kernel32.GetUserDefaultUILanguage.restype = c_long
        windll.kernel32.GetUserDefaultUILanguage.argtypes = []
        language_id = windll.kernel32.GetUserDefaultUILanguage()

        if language_id == 1049:
            lang = {
                "error": "Ошибка JitTools",
                "error_desc": "Произошла ошибка",
                "error_desc_info": "Информация об ошибке скопирована в буфер обмена. Передайте ее разработчику!",
                "update_title": "Доступно обновление",
                "update_description": "Доступна новая версия JitTools",
                "update_info": "Открыть страницу загрузки",
                "select_file": "Выберите файл",
                "select_to_file": "Успешно сохранено в файл",
                "empty_input": "Вы ничего не ввели",
                "enter_encrypted_code": "Введите зашифрованный код",
                "web_tools": "Веб-инструменты",
                "start": "Запустить",
                "open": "Открыть",
                "instructions": "Инструкции",
                "compilation": "Компиляция",
                "deobfuscation": "Деобфускация",
                "running_code": "Запуск кода",
                "code_analysis": "Анализ кода",
                "checkbox_description": "Эта функция будет работать с скриптами, перемещенными при помощи Drag&Drop или в аргументе командной строки.",
                "unprotector": "Анпротектор",
                "decompiler": "Декомпилятор",
                "decompilation": "Декомпиляция",
                "checkbox_name": "Применить ко всем скриптам",
                "apply_decompiler": "Применить декомпилятор",
            }
        else:
            lang = {
                "error": "Error JitTools",
                "error_desc": "An error has occurred",
                "error_desc_info": "The debugging information has been copied to the clipboard. Send it to the developer!",
                "update_title": "Update is available",
                "update_description": "A new version of JitTools is available | ",
                "update_info": "Open the download page",
                "select_file": "Select a file",
                "select_to_file": "Successfully saved to file",
                "empty_input": "Empty input",
                "enter_encrypted_code": "Enter encrypted code",
                "web_tools": "Web Tools",
                "start": "Start",
                "open": "Open",
                "instructions": "Instructions",
                "compilation": "Compilation",
                "deobfuscation": "Deobfuscation",
                "running_code": "Running Code",
                "code_analysis": "Code Analysis",
                "checkbox_description": "This function will work with all scripts moved using Drag&Drop or in response to a command line argument.",
                "unprotector": "Unprotector",
                "decompiler": "Decompiler",
                "decompilation": "Decompilation",
                "checkbox_name": "Apply to all scripts",
                "apply_decompiler": "Apply decompiler",
            }

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
                    lang["update_title"],
                    f"{lang["update_description"]} v{new_version}\n\n{log}\n\n{lang['update_info']}?"
                )
                if response:
                    open_browser("https://github.com/untitled-1111/JitTools/releases")
                    sys.exit()

        except OSError: # если интернет отсутствует
            pass

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

    tkinter.messagebox.showinfo(lang["error"], f"{lang["error_desc"]}:\n[{e.__traceback__.tb_lineno}]: {e} \n\n{lang['error_desc_info']}")
    windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL
    sys.exit()
