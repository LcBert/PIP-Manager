from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import os

import threads
import package_info_page


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("PIP Manager")
        self.geometry("450x500")
        self.iconbitmap("img/appicon.ico")
        self.protocol("WM_DELETE_WINDOW", self.xquit)
        self.resizable(False, True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.font = ("Arial", 12)

        self.reload_image = PhotoImage(file="img/reload.png")
        self.install_image = PhotoImage(file="img/install.png")
        self.trash_image = PhotoImage(file="img/trash.png")
        self.browse_image = PhotoImage(file="img/browse.png")
        self.folder_image = PhotoImage(file="img/folder.png")

        self.index_frame = Frame(self)
        self.index_frame.grid(column=0, row=0, padx=5, pady=(5, 0), sticky="ew")
        self.index_frame.grid_columnconfigure(1, weight=1)

        Label(self.index_frame, text="Search", font=self.font).grid(column=0, row=0, sticky="w")

        self.search_input = Entry(self.index_frame, font=self.font, border=1, relief="solid")
        self.search_input.grid(column=1, row=0, padx=5, sticky="ew")
        self.search_input.bind("<KeyRelease>", lambda _: self.load_list_table(search=self.search_input.get()))
        self.search_input.bind("<ButtonRelease>", lambda _: self.load_list_table(search=self.search_input.get()))
        self.search_input.bind("<Button-3>", lambda _: self.search_input.delete(0, END))

        self.reload_button = Button(self.index_frame, image=self.reload_image, command=lambda: self.load_list_table(reload=True))
        self.reload_button.grid(column=3, row=0, padx=(5, 0))

        self.install_button = Button(self.index_frame, image=self.install_image, command=lambda: self.install_package())
        self.install_button.grid(column=2, row=0, padx=(5, 0))

        self.list_frame = Frame(self, border=1, relief="solid")
        self.list_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)

        self.list_table = ttk.Treeview(self.list_frame, columns=("Package", "Version"), show="headings")
        self.list_table.heading("Package", text="Package")
        self.list_table.heading("Version", text="Version")
        self.list_table.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        self.list_table.bind("<<TreeviewSelect>>", lambda _: self.list_table_check_selection())
        self.list_table.bind("<Double-1>", lambda _: package_info_page.Page(self, self.list_table.item(self.list_table.selection())["values"][0]))
        self.list_table.tag_configure("even", background="#D3D3D3")
        self.list_table.tag_configure("odd", background="#FFFFFF")

        self.list_table_scrollbar = ttk.Scrollbar(self.list_frame, orient=VERTICAL, command=self.list_table.yview)
        self.list_table_scrollbar.grid(column=1, row=0, sticky="ns")
        self.list_table.configure(yscroll=self.list_table_scrollbar.set)

        self.command_frame = Frame(self)
        self.command_frame.grid(column=0, row=2, padx=5, pady=(0, 5), sticky="ew")

        self.delete_button = Button(self.command_frame, image=self.trash_image, state="disabled", command=lambda: threads.uninstall_package(self, self.list_table.item(self.list_table.selection())["values"][0]).start())
        self.delete_button.grid(column=0, row=0, padx=(0, 5))

        self.load_list_table(reload=True)

    def load_list_table(self, reload: bool = False, search: str = ""):
        if reload:
            threads.reload_packages(self).start()
        else:
            self.list_table.delete(*self.list_table.get_children())
            with open("packages.txt", "r") as file:
                file.readline()
                file.readline()
                for index, line in enumerate(file.readlines()):
                    label_text: list = line.split()
                    if search.lower() in label_text[0].lower().strip():
                        if index % 2 == 0:
                            tag = ("even")
                        else:
                            tag = ("odd")
                        try:
                            self.list_table.insert("", "end", values=(label_text[0].strip(), label_text[1].strip()), tags=tag)
                        except Exception as e:
                            print(e)
            self.reload_button.configure(state="active")

    def install_package(self):
        package_name = simpledialog.askstring("Install Package", "Enter the package name:")
        if package_name is not None:
            threads.install_package(self, package_name).start()

    def list_table_check_selection(self):
        if self.list_table.selection():
            self.delete_button.configure(state="active")
        else:
            self.delete_button.configure(state="disabled")

    def start(self):
        self.mainloop()

    def xquit(self):
        # if os.path.exists("packages.txt"):
        #     os.remove("packages.txt")
        self.quit()


if __name__ == "__main__":
    app = App()
    app.start()
