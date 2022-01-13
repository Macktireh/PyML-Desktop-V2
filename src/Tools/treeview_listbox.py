import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from Tools.settings import DefTools


class FilTreeView:

    def fil(self, treeview, df):
        # if VarCheckBtn.get():
        #     df.reset_index(inplace=True)
        #     df = df.rename(columns={"index": "Id"})

        global count
        count = 0

        treeview.tag_configure("oddrow", background="white")
        treeview.tag_configure("evenrow", background="#D3D3D3")

        # vider le treeview
        treeview.delete(*treeview.get_children())

        treeview["column"] = list(df.columns)
        treeview["show"] = "headings"

        for column in treeview["columns"]:
            treeview.column(column, anchor="w")
            treeview.heading(column, anchor="w", text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            if count % 2 == 0:
                treeview.insert(
                    "",
                    "end",
                    iid=count,
                    values=row,
                    tags=("evenrow",),
                )
            else:
                treeview.insert(
                    "",
                    "end",
                    iid=count,
                    values=row,
                    tags=("oddrow",),
                )
            count += 1

        treeview.insert("", "end", values="")

        

class FilListBox:
    def fil(self, Lbox, df):
        Lbox.delete(0, "end")
        for id, column in enumerate(df.columns):
            # v = self.VerifType(df, column)
            values_listbox = f" {column}  : {DefTools.CheckType(self, df, column)}      "
            Lbox.insert(id, values_listbox)