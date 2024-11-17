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
"""

try: 
  import os
  import sys
  import ctypes
  import tkinter as tk
  import socket
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

          # configure window
          self.title(f"JitTools v{version}")

          customtkinter.set_widget_scaling(1.1) # текст мелкий пиздец, нихуя не видно
          screen_width = self.winfo_screenwidth()
          screen_height = self.winfo_screenheight()
          x = (screen_width - 700) // 2
          y = (screen_height - 380) // 2 + 20
          self.geometry(f"700x380+{x}+{y}")

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
          self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

          self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn2_event, text="Деобфускация")
          self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

          self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.btn3_event, text="Анализ кода")
          self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

          self.sidebar_button_1.invoke()

    def open_input_dialog_event(self):
          dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
          print("CTkInputDialog:", dialog.get_input())

    def btn1_event(self):
          self.tabview = customtkinter.CTkTabview(self, width=500)
          self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

          self.tabview.add("Декомпилятор")
          self.tabview.add("Анпротектор")

          self.tabview.tab("Декомпилятор").grid_columnconfigure(0, weight=1)
          self.tabview.tab("Анпротектор").grid_columnconfigure(0, weight=1)

          self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Декомпилятор"), dynamic_resizing=False,
                                                          values=["LuaJIT Fork", "Python Fork"])
          self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

          self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Декомпилятор"), command=lambda: self.decompile_event(self.optionmenu_1.get()), text="Запустить", width=100)
          self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)


          self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Анпротектор"), dynamic_resizing=False,
                                                          values=["Unprot v2.1"])
          self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

          self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Анпротектор"), command=lambda: self.unprot_event(self.optionmenu_2.get()), text="Запустить", width=100)
          self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)

          # set default values
          self.optionmenu_1.set("LuaJIT Fork")
          self.optionmenu_2.set("Unprot v2.1")

    def btn2_event(self):
          self.tabview = customtkinter.CTkTabview(self, width=500)
          self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

          self.tabview.add("Запуск кода")
          self.tabview.add("Деобфускаторы")

          self.tabview.tab("Запуск кода").grid_columnconfigure(0, weight=1)
          self.tabview.tab("Деобфускаторы").grid_columnconfigure(0, weight=1)

          self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Запуск кода"), dynamic_resizing=False,
                                                          values=["Moonsec Dump", "Hook Obf", "Debugger", "XOR Unpack"])
          self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

          self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Запуск кода"), command=lambda: self.debug_event(self.optionmenu_1.get()), text="Запустить", width=100)
          self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)


          self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Деобфускаторы"), dynamic_resizing=False,
                                                          values=["Base64 Deobf", "Shit Deobf"])
          self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

          self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Деобфускаторы"), command=lambda: self.deobf_event(self.optionmenu_1.get()), text="Запустить", width=100)
          self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)

          # set default values
          self.optionmenu_1.set("Moonsec Dump")
          self.optionmenu_2.set("Base64 Deobf")

    def btn3_event(self):
          self.tabview = customtkinter.CTkTabview(self, width=500)
          self.tabview.grid(row=0, column=1, rowspan=4, sticky="nsew")

          self.tabview.add("Компиляция")
          self.tabview.add("Просмотр инструкций")

          self.tabview.tab("Компиляция").grid_columnconfigure(0, weight=1)
          self.tabview.tab("Просмотр инструкций").grid_columnconfigure(0, weight=1)

          self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Компиляция"), dynamic_resizing=False,
                                                          values=["LuaJIT Compiler", "Joiner"])
          self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

          self.button_tab_1 = customtkinter.CTkButton(self.tabview.tab("Компиляция"), command=lambda: self.compile_event(self.optionmenu_1.get()), text="Запустить", width=100)
          self.button_tab_1.grid(row=1, column=0, padx=20, pady=2)

          self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Просмотр инструкций"), dynamic_resizing=False,
                                                          values=["BCViewer", "Luad", "ASM"])
          self.optionmenu_2.grid(row=0, column=0, padx=20, pady=(20, 10))

          self.button_tab_2 = customtkinter.CTkButton(self.tabview.tab("Просмотр инструкций"), command=lambda: self.instruct_event(self.optionmenu_1.get()), text="Запустить", width=100)
          self.button_tab_2.grid(row=1, column=0, padx=20, pady=2)

          # set default values
          self.optionmenu_1.set("LuaJIT Compiler")
          self.optionmenu_2.set("BCViewer")


    def decompile_event(self, _):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title="Выберите файл для декомпиляции", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
        if not file_path:
            sys.exit()

        if self.optionmenu_1.get() == "LuaJIT Fork":
            modules.LJD_Decompiler.ljd_decompiler(file_path)

        elif self.optionmenu_1.get() == "Python Fork":
            modules.LJD_Decompiler.py_decompiler(file_path)

    def unprot_event(self, _):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title="Выберите файл для снятия прота", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
        if not file_path:
            sys.exit()

        if self.optionmenu_2.get() == "Unprot v2.1":
            modules.unprot.unprot_2(file_path)

    def debug_event(self, _):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
        if not file_path:
            sys.exit()

        if self.optionmenu_1.get() == "Moonsec Dump":
            modules.debug.moonsecdump(file_path)

        elif self.optionmenu_1.get() == "Hook Obf":
            modules.debug.hookobf(file_path)

        elif self.optionmenu_1.get() == "Debugger":
            modules.debug.debugger(file_path)

        elif self.optionmenu_1.get() == "XOR Unpack":
            modules.debug.xorunpack(file_path)

    def deobf_event(self, _):
        from tkinter import simpledialog, filedialog

        if self.optionmenu_2.get() == "Base64 Deobf":
            input = simpledialog.askstring("Base64 Deobf", "Введите зашифрованный код, и результат будет отображен в консоли: ")
            modules.deobf.base64d(input)

        elif self.optionmenu_2.get() == "Shit Deobf":
            file_path = filedialog.askopenfilename(title="Выберите файл для деобфускации", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
            if not file_path:
                sys.exit()

            modules.deobf.shitd(file_path)

    def compile_event(self, _):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
        if not file_path:
            sys.exit()

        if self.optionmenu_1.get() == "LuaJIT Compiler":
            modules.LJD_Compiler.compiler(file_path)

        elif self.optionmenu_1.get() == "Joiner":
            modules.LJD_Compiler.joiner(file_path)


    def instruct_event(self, _):
        if self.optionmenu_2.get() == "BCViewer":
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
            if not file_path:
                sys.exit()

            modules.instruct.bcviewer(file_path)

        elif self.optionmenu_2.get() == "Luad":
            modules.instruct.luad()

        elif self.optionmenu_2.get() == "ASM":
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac;*.txt")])
            if not file_path:
                sys.exit()
                
            modules.instruct.asm(file_path)
        
  if __name__ == "__main__":
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

    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    root = tk.Tk()

    # проверка наличия интернета и новой версии (авто-обновления нету)
    try:
        socket.create_connection(("www.google.com", 80))
        internet_available = True

    except OSError:
        pass

    if internet_available:
        response = get("https://raw.githubusercontent.com/untitled-1111/JitTools/refs/heads/master/check_update")
        response.raise_for_status()
        response_lines = response.text.splitlines()
        new_version = response_lines[0].strip()
        log = "\n".join(response_lines[1:])

        if float(new_version) > float(version):
            root.withdraw()
            response = tk.messagebox.askyesno(
                "Доступно обновление",
                f"Доступна новая версия JitTools v{new_version}\n\n{log}\n\nОткрыть страницу загрузки?"
            )
            if response:
                import webbrowser
                webbrowser.open("https://github.com/untitled-1111/JitTools/releases")
                sys.exit()

    root.destroy()
    app = App()
    app.mainloop()

except Exception as e:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    print(f"[ERROR] {str(e)}")
    input("[!] В JitTools произошла ошибка, сообщите о ней автору!")