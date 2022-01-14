import os
import pandas as pd
import tkinter as tk
import psycopg2
import sys

from tkinter import PhotoImage
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
from GetData.Previous import PreviousData
from Tools.Btns import LabelEntry

sys.path.append('../')
load_env = load_dotenv()


class PostgreSQL:
    def __init__(self, root, tv_All_Data, Lbox, VarNbLigneCol, RomeveCol, transformBtn, saveBtn, exportBtn, button_executor_fx, button_remove_rows, data_origine, data_pre):
        self.root = root

        self.window_postgresql = tk.Toplevel(self.root)
        self.window_postgresql.grab_set()
        self.window_postgresql.title("PostgreSQL database")
        self.window_postgresql.iconbitmap("media/logo.ico")
        self.window_postgresql.geometry("500x600+15+15")
        self.window_postgresql.resizable(width=False, height=False)
        
        self.tv_All_Data = tv_All_Data
        self.Lbox = Lbox
        self.VarNbLigneCol = VarNbLigneCol
        self.RomeveCol = RomeveCol
        self.transformBtn = transformBtn
        self.saveBtn = saveBtn
        self.exportBtn = exportBtn
        self.button_executor_fx = button_executor_fx 
        self.button_remove_rows = button_remove_rows


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
        self.Entry_host = LabelEntry(self.window_postgresql, label_text='Host', textvar=os.getenv('HOST'), x=0.28, y=0.2, width=40, show='')

        # Data Base Name
        self.Entry_dbname = LabelEntry(self.window_postgresql, label_text='Database', textvar=os.getenv('DBNAME'), x=0.28, y=0.25, width=40, show='')

        # Port
        self.Entry_port = LabelEntry(self.window_postgresql, label_text='Port', textvar=os.getenv('PORT'), x=0.28, y=0.3, width=40, show='')

        # Username
        self.Entry_username = LabelEntry(self.window_postgresql, label_text='Username', textvar=os.getenv('USER'), x=0.28, y=0.35, width=40, show='')

        # Password
        self.Entry_password = LabelEntry(self.window_postgresql, label_text='Password', textvar=os.getenv('PASSWORD'), x=0.28, y=0.35, width=40, show='*')

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
                PreviousData(self.root, self.data_pre, self.path_import, self.tv_All_Data, self.Lbox, self.VarNbLigneCol, self.RomeveCol, self.transformBtn, self.saveBtn, self.exportBtn, self.button_executor_fx, self.button_remove_rows)
                self.window_postgresql.destroy()
            # except :
                # tk.messagebox.showerror("Information", "Echec connexion !")
        else:
            tk.messagebox.showerror("Information", "some fields are not filled")
