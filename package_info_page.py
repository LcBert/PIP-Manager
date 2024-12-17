from tkinter import *
from tkinter import ttk
import subprocess
import webbrowser

info_values = {
    "Name": "",
    "Version": "",
    "Summary": "",
    "Home-page": "",
    "Author": "",
    "Author-email": "",
    "License": "",
    "Location": ""
}


class Page():
    def __init__(self, app: Tk, packages_name: str):
        self.app = app
        self.packages_name = packages_name
        self.page = Toplevel(app)
        self.page.title("Select Packages")
        self.page.iconbitmap("img/appicon.ico")
        self.page.geometry("550x235")
        self.page.resizable(False, False)
        self.page.transient(app)

        self.page.grid_columnconfigure(0, weight=1)
        self.page.grid_rowconfigure(0, weight=1)

        self.create_page()
        self.load_info()
        self.load_info_table()

    def create_page(self):
        self.info_table = ttk.Treeview(self.page, columns=("Info", "Value"), show="headings")
        self.info_table.heading("Info", text="Info")
        self.info_table.heading("Value", text="Value")
        self.info_table.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        self.info_table.column("Info", width=-130)
        self.info_table.tag_configure("even", background="#D3D3D3")
        self.info_table.tag_configure("odd", background="#FFFFFF")

        self.button_frame = Frame(self.page)
        self.button_frame.grid(column=0, row=1, padx=5, pady=(0, 5), sticky="ew")

        self.open_package_folder_button = Button(self.button_frame, image=self.app.folder_image, command=lambda: self.open_package_folder())
        self.open_package_folder_button.grid(column=0, row=0, padx=(0, 5), sticky="ew")

        self.open_package_browser_button = Button(self.button_frame, image=self.app.browse_image, command=lambda: self.open_package_browser())
        self.open_package_browser_button.grid(column=1, row=0, padx=(0, 5), sticky="ew")

    def load_info(self):
        show_output = subprocess.check_output(f"pip show {self.packages_name}").decode(encoding='utf-8', errors='ignore')
        for value in info_values.items():
            info_values[value[0]] = show_output.split(f"{value[0]}: ")[1].split("\n")[0].strip()

    def load_info_table(self):
        self.info_table.delete(*self.info_table.get_children())
        for index, value in enumerate(info_values.items()):
            if index % 2 == 0:
                tag = ("even")
            else:
                tag = ("odd")
            self.info_table.insert("", "end", values=(value[0], value[1]), tags=tag)

    def open_package_folder(self):
        if (info_values["Location"] != ""):
            subprocess.Popen(f'explorer "{info_values["Location"]}\\{info_values["Name"]}"')

    def open_package_browser(self):
        if (info_values["Home-page"] != ""):
            webbrowser.open(info_values["Home-page"])
