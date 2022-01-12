import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import PhotoImage
from tkinter.scrolledtext import ScrolledText
import psycopg2
import sys

sys.path.append('../')


class LabelEntry:
    def __init__(self, root, label_text, textvar, show, x, y, width):
        self.root = root
        self.label_text = label_text
        self.textvar = textvar
        self.show = show
        self.x = x
        self.y = y
        self.width = width
        
        self.label = tk.Label(
            self.root, text=self.label_text, font=("Helvetica", 10)
        ).place(relx=0.07, rely=0.2)
        self.VarEntry = tk.StringVar()
        self.VarEntry.set(self.textvar)
        self.entry = tk.Entry(
            self.root, textvariable=self.VarEntry, width=40, show=self.show
        )
        self.entry.place(relx=self.x, rely=self.y)
        
    def get_value_entry(self):
        return self.entry.get()

    def set_value_entry(self, value):
        self.VarEntry.set(value)



class Api:
    def __init__(self, root):
        self.root = root

        self.window_postgresql = tk.Toplevel(self.root)
        self.window_postgresql.grab_set()
        self.window_postgresql.title("PostgreSQL database")
        self.window_postgresql.iconbitmap("media/logo.ico")
        self.window_postgresql.geometry("500x600+15+15")
        self.window_postgresql.resizable(width=False, height=False)


        # Importation de l'icone de progresql
        self.img = PhotoImage(file="media/postgresql.png")
        self.img = self.img.subsample(35, 35)

        # afficher l'icone de progresql
        self.print_img = tk.Label(
            self.window_postgresql, image=self.img, width=90, height=90
        )
        self.print_img.place(relx=0.01, rely=0.01)

        #  label de titre progresql
        self.lbl_title = tk.Label(
            self.window_postgresql, text="PostgreSQL database", font=("Helvetica", 16)
        )
        self.lbl_title.place(relx=0.25, rely=0.05)

        # Host
        self.Entry_host = LabelEntry(self.window_postgresql, label_text='Host', textvar='localhost', x=0.28, y=0.2, width=40, show='')

        # Data Base Name
        self.Entry_dbname = LabelEntry(self.window_postgresql, label_text='Database', textvar='dvdrental', x=0.28, y=0.25, width=40, show='')

        # Port
        self.Entry_port = LabelEntry(self.window_postgresql, label_text='Port', textvar='5444', x=0.28, y=0.3, width=40, show='')

        # Username
        self.Entry_username = LabelEntry(self.window_postgresql, label_text='Username', textvar='enterprisedb', x=0.28, y=0.35, width=40, show='')

        # Password
        self.Entry_password = LabelEntry(self.window_postgresql, label_text='Password', textvar='charco97', x=0.28, y=0.35, width=40, show='*')

        # label Text Widget pour ecrire su sql
        self.lbl_sql = tk.Label(
            self.window_postgresql,
            text="Please write your SQL query",
            font=("Helvetica", 12),
        ).place(relx=0.1, rely=0.48)
        # Text Widget pour ecrire su sql
        self.text_sql = ScrolledText(self.window_postgresql, font=("Helvetica", 10))
        self.text_sql.place(relx=0.1, rely=0.52, relwidth=0.8, relheight=0.35)

        self.OkPogreSQL = tk.Button(
            self.window_postgresql,
            text="OK",
            background="#6DA3F4",
            activebackground="#0256CD",
            foreground="white",
            activeforeground="white",
            width=12,
            height=1,
            command=self.Requete_SQL,
        )
        self.OkPogreSQL.place(relx=0.31, rely=0.9)

        self.CacelPogreSQL = tk.Button(
            self.window_postgresql,
            text="Cancel",
            background="#CCCCCC",
            width=12,
            height=1,
            command=self.Cancel_widow_prosgresql,
        )
        self.CacelPogreSQL.place(relx=0.50, rely=0.9)
    
    
    def Cancel_widow_prosgresql(self):
        self.window_postgresql.destroy()

    def Requete_SQL(self):

        if (
            self.text_sql.get("1.0", "end-1c")
            and self.Entry_host.get_value_entry()
            and self.Entry_port.get_value_entry()
            and self.Entry_dbname.get_value_entry()
            and self.Entry_username.get_value_entry()
            and self.Entry_password.get_value_entry()
        ):
            # try:

                connexion = psycopg2.connect(
                    dbname=f"{self.Entry_dbname.get_value_entry()}",
                    user=f"{self.Entry_username.get_value_entry()}",
                    password=f"{self.Entry_password.get_value_entry()}",
                    host=f"{self.Entry_host.get_value_entry()}",
                    port=f"{self.Entry_port.get_value_entry()}",
                )
                cur = connexion.cursor()
                cur.execute(f"{self.text_sql.get('1.0', 'end-1c')}")
                row = cur.fetchall()

                col_names = []
                for elt in cur.description:
                    col_names.append(elt[0])

                df = pd.DataFrame(
                    row,
                    columns=col_names,
                )
                df.reset_index(inplace=True)
                df = df.rename(columns={"index": "Id"})

                self.data_origine = df
                self.data_pre = self.data_origine.copy()

                self.path_import = f"Table data {self.Entry_dbname.get_value_entry()} from the PostgreSQL database "

                from App import PyData
                PyData.preview_data(self, self.path_import, self.data_pre)
                self.window_postgresql.destroy()
            # except :
                # tk.messagebox.showerror("Information", "Echec connexion !")
        else:
            tk.messagebox.showerror("Information", "some fields are not filled")
