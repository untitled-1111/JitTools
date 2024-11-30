# JitTools Installer 
# https://www.blast.hk/threads/223498/

links = {
    "Visual C++ All-In-One": "https://github.com/abbodi1406/vcredist/releases/download/v0.85.0/VisualCppRedist_AIO_x86_x64.exe",
    ".NET Core 3.1 SDK": "https://download.visualstudio.microsoft.com/download/pr/b70ad520-0e60-43f5-aee2-d3965094a40d/667c122b3736dcbfa1beff08092dbfc3/dotnet-sdk-3.1.426-win-x64.exe"
}

def install_jittools():
    try:
        windll.kernel32.SetConsoleTitleW("JitTools Installer")
        print("\n\033[90m-> JitTools Installer\033[0m")

        all_successful = True
        for link in links.values():
            response = head(link)
            if response.status_code not in (200, 302):
                all_successful = False
                raise Exception(f"\033[91mОшибка {response.status_code} при запросе {link}\033[0m")

        if all_successful:
            print("\033[92mСписки системных и Python модулей загружены.\n\033[0m")
        
        match = search(r"JitTools v\d+\.\d+\.zip", " ".join(listdir()))
        if not match:
            raise Exception("\033[91mАрхив JitTools не найден.\033[0m")

        version = match.group().split()[1]
        print(f"Архив JitTools {version} найден, разархивируем...")

        with ZipFile(match.group()) as zf:
            total_files = len(zf.namelist())
            for i, file in enumerate(zf.namelist(), start=1):
                if path.exists(file):
                    remove(file)
                zf.extract(file)
                progress = int(i / total_files * 100)
                print(f"\r[\033[90m{'#' * progress}\033[0m\033[90m{' ' * (100 - progress)}\033[0m] \033[94m{progress:>2}%\033[0m", end="", flush=True)
        
        system('cls')
        print("\n\033[90m-> JitTools Installer\033[0m")
        print("\n\033[92mАрхив успешно разархивирован.\033[0m")

        system('cls')
        print("\n\033[90m-> JitTools Installer\033[0m")

        answer = messagebox.askyesno("Установка системных библиотек", "Установить системные библиотеки Visual C++ и .NET Core?")

        if answer:
            for name, link in links.items():
                print(f"\n\033[96mЗагрузка {name}...\033[0m")
                file_name = link.split('/')[-1]

                if not path.exists(file_name):
                    response = get(link, stream=True)
                    total_size = int(response.headers.get('content-length', 0))
                    with open(file_name, 'wb') as f:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress = int(downloaded / total_size * 100)
                                print(f"\r[\033[90m{'#' * progress}\033[0m\033[90m{' ' * (100 - progress)}\033[0m] \033[94m{progress:>2}%\033[0m", end="", flush=True)

                print(f"\n\033[92mМодуль {name} успешно загружен.\033[0m")
                print(f"\033[96mЗапуск {name}...\033[0m")

                windll.shell32.ShellExecuteW(None, "runas", file_name, None, None, 1)

        else:
            input("\033[91mДля закрытия утилиты нажмите ENTER...\033[0m")
            exit()
            
        print(f"\nУстановка успешно завершена, открываем папку...")
        startfile(path.abspath('.'))
        input("Для закрытия утилиты нажмите ENTER...")
        exit()

    except Exception as e:
        input(f"\033[91mПроизошла ошибка: {str(e)}\033[0m")
        exit()

if __name__ == "__main__":
    from os import system, path, startfile, listdir, remove
    system('pip install -r requirements.txt')

    from subprocess import run, PIPE
    from sys import exit
    from requests import head, get
    from re import search
    from zipfile import ZipFile
    from tkinter import messagebox
    from ctypes import windll

    system('cls')
    install_jittools()