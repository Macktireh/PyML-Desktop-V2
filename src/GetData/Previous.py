import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from Tools.settings import DefTools
from Tools.treeview_listbox import FilTreeView, FilListBox


class PreviousData:
    def __init__(self, root, df, path, tv_All_Data, Lbox, VarNbLigneCol,RomeveCol, transformBtn, saveBtn, exportBtn, button_executor_fx, button_remove_rows):
        self.root = root
        self.df = df
        self.path = path
        self.tv_All_Data = tv_All_Data
        self.Lbox = Lbox
        self.VarNbLigneCol = VarNbLigneCol
        self.RomeveCol = RomeveCol
        self.transformBtn = transformBtn
        self.saveBtn = saveBtn
        self.exportBtn = exportBtn
        self.button_remove_rows = button_remove_rows
        self.button_executor_fx = button_executor_fx
        
        self.preview = tk.Toplevel(self.root)
        self.preview.grab_set()
        self.preview.title("Previous Data")
        self.preview.iconbitmap("media/logo.ico")
        self.preview.geometry("600x250+15+15")
        self.preview.resizable(width=False, height=False)

        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

        def switchButtonState(RomeveCol, transformBtn, saveBtn, exportBtn, button_executor_fx, button_remove_rows):

            """Cette fonction de switcher les boutons dans le volet transformation de deactive en active. Elle est appeler lorsque on clique on valide le chargement de données (le bouton ok dans le preview data)"""

            if RomeveCol["state"] == "disabled":
                RomeveCol["state"] = "normal"
            else:
                RomeveCol["state"] = "normal"

            # if self.Btn_Change_type_col["state"] == "disabled":
            #     self.Btn_Change_type_col["state"] = "normal"
            # else:
            #     self.Btn_Change_type_col["state"] = "normal"

            if transformBtn["state"] == "disabled":
                transformBtn["state"] = "normal"
            else:
                transformBtn["state"] = "normal"

            if saveBtn["state"] == "disabled":
                saveBtn["state"] = "normal"
            else:
                saveBtn["state"] = "normal"

            if exportBtn["state"] == "disabled":
                exportBtn["state"] = "normal"
            else:
                exportBtn["state"] = "normal"

            if button_executor_fx["state"] == "disabled":
                button_executor_fx["state"] = "normal"
            else:
                button_executor_fx["state"] = "normal"

            if button_remove_rows["state"] == "disabled":
                button_remove_rows["state"] = "normal"
            else:
                button_remove_rows["state"] = "normal"

        def ok_data_V():

            """Cette fonction valide les données et affiche toutes les données. Elle est relier au bouton ok pour valider"""

            # self.fil_data_to_treeview_listbox(self.df, w="all")
            FilTreeView.fil(self, self.tv_All_Data, df)
            FilListBox.fil(self, self.Lbox, df)
            DefTools.Fonc_label_nbr_ligne_et_col(self, self.df, self.VarNbLigneCol)
            switchButtonState(self.RomeveCol, self.transformBtn, self.saveBtn, self.exportBtn, self.button_executor_fx, self.button_remove_rows)
            self.preview.destroy()

            return self.df

        frame1 = tk.LabelFrame(self.preview, text=f"{self.path}")
        frame1.place(height=170, width=530, rely=0.02, relx=0.05)

        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)

        # commande signifie mettre à jour la vue de l'axe y du widget
        treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)

        # commande signifie mettre à jour la vue axe x du widget
        treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)

        # affecter les barres de défilement au widget Treeview
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

        # faire en sorte que la barre de défilement remplisse l'axe x du widget Treeview
        treescrollx.pack(side="bottom", fill="x")

        # faire en sorte que la barre de défilement remplisse l'axe y du widget Treeview
        treescrolly.pack(side="right", fill="y")

        fram_check_btn_lbl = tk.Frame(self.preview)
        fram_check_btn_lbl.place(relx=0.05, rely=0.73)

        self.VarCheckBtn_add_index = tk.BooleanVar()
        self.VarCheckBtn_add_index.set(True)
        CheckBtn_add_index = tk.Checkbutton(
            fram_check_btn_lbl,
            variable=self.VarCheckBtn_add_index,
            command=None,
        )
        CheckBtn_add_index.grid(row=0, column=0)

        text_checkbtn_add_index = tk.Label(
            fram_check_btn_lbl, text="Add an index column"
        )
        text_checkbtn_add_index.grid(row=0, column=1)

        OkBtn_data = tk.Button(
            self.preview,
            # text="Ok",
            # background="#40A497",
            # activeforeground="white",
            # activebackground="#40A497",
            text="OK",
            background="#6DA3F4",
            activebackground="#0256CD",
            foreground="white",
            activeforeground="white",
            width=12,
            height=1,
            command=ok_data_V,
        ).place(relx=0.32, rely=0.87)

        Cancel_data = tk.Button(
            self.preview,
            text="Cancel",
            background="#CCCCCC",
            width=12,
            height=1,
            command=None,
            # command=self.CancelPreviwData,
        ).place(relx=0.48, rely=0.87)

        clear_data()
        tv1["column"] = list(self.df.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.column(column, anchor="center")
            tv1.heading(column, text=column)

        self.df_rows = self.df.head().to_numpy().tolist()
        for row in self.df_rows:
            tv1.insert("", "end", values=row)

        return None