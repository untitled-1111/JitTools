# JitTools Installer 
# https://github.com/untitled-1111/JitTools

links = {
    "Visual C++ All-In-One": "https://github.com/abbodi1406/vcredist/releases/download/v0.85.0/VisualCppRedist_AIO_x86_x64.exe",
    ".NET Core 3.1 SDK": "https://download.visualstudio.microsoft.com/download/pr/b70ad520-0e60-43f5-aee2-d3965094a40d/667c122b3736dcbfa1beff08092dbfc3/dotnet-sdk-3.1.426-win-x64.exe"
}

class install():
    def __init__(self):
        install.check_links()
        install.check_archive()
        install.extract_archive()
        install.install_modules()
        install.successfully()

    def check_links():
        print("\n\033[90m-> JitTools Installer\033[0m")

        for link in links.values():
            response = head(link)
            if response.status_code not in (200, 302):
                system('cls')
                print(f"\033[91mОшибка {response.status_code} при запросе {link}\033[0m")

                input("Для закрытия утилиты нажмите ENTER.")
                exit()

        print("\033[92mСписки системных и Python модулей загружены.\n\033[0m")

    def check_archive():
        if not match:
            system('cls')
            print("\033[91mАрхив JitTools не найден.\033[0m")

            input("Для закрытия утилиты нажмите ENTER.")
            exit()

        print(f"Архив {version} найден, разархивируем...")
        clear("old_version")

    def extract_archive():
        try:
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

        except Exception as e:
            system('cls')
            print(f"\033[91mОшибка при разархивировании архива: {e}\033[0m")

            input("Для закрытия утилиты нажмите ENTER.")
            exit()

    def install_modules():
        system('cls')
        print("\n\033[90m-> JitTools Installer\033[0m")
        print(f"Скачивание системных модулей...")

        for name, link in links.items():
            print(f"\n\033[96mЗагрузка {name}...\033[0m")
            file_name = link.split('/')[-1]

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

            print(f"\n\033[92mМодуль {name} успешно загружен. Установка...\033[0m")
            
            # Silent Install
            if name == ".NET Core 3.1 SDK":
                windll.shell32.ShellExecuteW(None, "runas", file_name, "/install /quiet /norestart", None, 1)
                clear("dotnet-sdk-3.1.426-win-x64.exe")

            elif name == "Visual C++ All-In-One":
                windll.shell32.ShellExecuteW(None, "runas", file_name, "/y", None, None, 1)
                clear("VisualCppRedist_AIO_x86_x64.exe")

            system('cls')
            print("\n\033[90m-> JitTools Installer\033[0m")

    def successfully():
        system('cls')
        print("\n\033[90m-> JitTools Installer\033[0m")

        print(f"\nУстановка успешно завершена.")
        input("Для закрытия утилиты нажмите ENTER.")
        exit()


def clear(type):
    if type == "old_version":
        trash = [
            f"JitTools v{version.split(' ')[1]}.py",
            "JitTools.ini",
            "dumps",
            "gui",
            "modules",
            "tools"
        ]
    else:
        trash = [type]
    
    for item in trash:
        if path.exists(item):
            while True:
                try:
                    if path.isfile(item):
                        remove(item)
                    else:
                        for root, dirs, files in walk(item, topdown=False):
                            for file in files:
                                remove(path.join(root, file))
                            for dir in dirs:
                                rmdir(path.join(root, dir))
                        rmdir(item)
                    break

                except Exception:
                    sleep(3)

if __name__ == "__main__":
    from os import system, path, listdir, remove, walk, rmdir
    from ctypes import windll, byref, Structure, c_long
    from time import sleep

    # Setting Console
    windll.kernel32.SetConsoleTitleW("JitTools Installer")

    class RECT(Structure):
            _fields_ = [("left", c_long), ("top", c_long), ("right", c_long), ("bottom", c_long)]

    windll.user32.SetProcessDPIAware()
    rect = RECT()
    hwnd = windll.kernel32.GetConsoleWindow()
    windll.user32.GetWindowRect(hwnd, byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    cx = width // 2
    cy = height // 2
    x = (windll.user32.GetSystemMetrics(0) - width) // 2
    y = (windll.user32.GetSystemMetrics(1) - height) // 2
    windll.user32.MoveWindow(hwnd, x, y, width, height, 0)

    # Install and Import Python Modules
    print("\n-> JitTools Installer")
    print("Установка модулей Python...\n")
    system('pip install -r requirements.txt')

    from sys import exit
    from requests import head, get
    from re import search
    from zipfile import ZipFile

    # Get JitTools Version
    try:
        match = search(r"JitTools v\d+\.\d+\.zip", " ".join(listdir()))
        version = match.group()

    except Exception as e:
        system('cls')
        print("-> JitTools Installer\n")

        if str(e) == "'NoneType' object has no attribute 'group'":
            print(f"\033[91mОшибка: Архив JitTools не найден.\033[0m")
        else:
            print(f"\033[91mОшибка при проверке архива: {e}\033[0m")

        input("Для закрытия утилиты нажмите ENTER.")
        exit()

    # Start Install
    system('cls')
    install()