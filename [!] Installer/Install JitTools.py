# JitTools Installer 
# https://www.blast.hk/threads/223498/

from subprocess import run
from sys import executable
from os import system
from requests import head
from re import search
from os import listdir
from zipfile import ZipFile
from tkinter import messagebox
from os import remove
from subprocess import PIPE
from requests import get

links = {
    "Visual C++ All-In-One": "https://github.com/abbodi1406/vcredist/releases/download/v0.85.0/VisualCppRedist_AIO_x86_x64.exe",
    ".NET Core 3.1 SDK": "https://download.visualstudio.microsoft.com/download/pr/b70ad520-0e60-43f5-aee2-d3965094a40d/667c122b3736dcbfa1beff08092dbfc3/dotnet-sdk-3.1.426-win-x64.exe"
}

def install_jittools():
    try:
        from ctypes import windll
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
                from os import path
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
                module_name = list(links.keys())[list(links.values()).index(link)]
                if module_name == ".NET Core 3.1 SDK":
                    dotnet_version_check_script = """\
                    reg query "HKLM\\SOFTWARE\\Microsoft\\NET Framework Setup\\NDP\\v4" /s | findstr /R "Version"
                    """
                    result = run(dotnet_version_check_script, shell=True, stdout=PIPE, stderr=PIPE)
                    if result.returncode == 0:
                        print("\033[92mМодуль .NET Core 3.1 SDK уже установлен.\033[0m")
                        continue

                if module_name == "Visual C++ All-In-One":
                    vc_version_check_script = """\
                    reg query "HKLM\\SOFTWARE\\WOW6432Node\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64" /s
                    """
                    result = run(vc_version_check_script, shell=True, stdout=PIPE, stderr=PIPE)
                    if result.returncode == 0:
                        print("\n\033[92mМодуль Visual C++ All-In-One уже установлен.\033[0m")
                        continue

                print(f"\n\033[96mЗагрузка {module_name}...\033[0m")
                file_name = link.split('/')[-1]

                from os import path
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

                print(f"\n\033[92mМодуль {module_name} успешно загружен.\033[0m")
                print(f"\033[96mЗапуск {module_name}...\033[0m")

                from ctypes import windll
                windll.shell32.ShellExecuteW(None, "runas", file_name, None, None, 1)

        else:
            input("\033[91mДля закрытия утилиты нажмите ENTER...\033[0m")
            for file in ["JitTools {}.zip".format(version), "Install JitTools.py", "requirements.txt"]:
                try:
                    remove(file)
                except:
                    pass
            from sys import exit
            exit()
            
        print(f"\nУстановка успешно завершена, открываем папку...")

        from os import startfile, path
        from sys import exit

        startfile(path.abspath('.'))
        input("Для закрытия утилиты нажмите ENTER...")
        for file in ["JitTools {}.zip".format(version), "Install JitTools.py", "requirements.txt"]:
            try:
                remove(file)
            except:
                pass
        exit()

    except Exception as e:
        input(f"\033[91mПроизошла ошибка: {str(e)}\033[0m")
        exit()

if __name__ == "__main__":
    run([executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\033[92m   Модули успешно установлены.\033[0m")

    system('cls')
    install_jittools()