from tkinter import Tk
from tkinter import messagebox
import threading
import os


class reload_packages(threading.Thread):
    def __init__(self, app: Tk):
        super(reload_packages, self).__init__()
        self.daemon = True
        self.app: Tk = app

    def run(self):
        self.app.reload_button.config(state="disabled")
        os.system("pip list > packages.txt")
        self.app.load_list_table()
        self.app.reload_button.config(state="active")


class install_package(threading.Thread):
    def __init__(self, app: Tk, package_name: str):
        super(install_package, self).__init__()
        self.daemon = True
        self.app: Tk = app
        self.packages_name: str = package_name

    def run(self):
        self.app.reload_button.config(state="disabled")
        os.system(f"pip install --quiet {self.packages_name}")
        print(f"Installed {self.packages_name.upper()} successfully.")
        self.app.load_list_table(reload=True)


class uninstall_package(threading.Thread):
    def __init__(self, app: Tk, packages_name: str):
        super(uninstall_package, self).__init__()
        self.daemon = True
        self.app: Tk = app
        self.packages_name: str = packages_name

    def run(self):
        if messagebox.askokcancel("Uninstall Package", f"Are you sure you want to uninstall {self.packages_name.upper()}?"):
            self.app.reload_button.config(state="disabled")
            os.system(f"pip uninstall --yes --quiet {self.packages_name}")
            print(f"Uninstalled {self.packages_name.upper()} successfully.")
            self.app.load_list_table(reload=True)
