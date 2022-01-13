import numpy as np
import pandas as pd


class DefTools:
    
    def CheckType(self, df, column):
        if np.dtype(df[column]) == "object":
            typ = "string"
        elif np.dtype(df[column]) in ["int32", "int64"]:
            typ = "integer"
        elif np.dtype(df[column]) in ["float32", "float32", "float"]:
            typ = "float"
        elif np.dtype(df[column]) in [
            "datetime64[ns]",
            "datetime32[ns]",
            "datetime64",
            "datetime32",
            "datetime",
            "date",
        ]:
            typ = "datetime"
        else:
            typ = np.dtype(df[column])
        return typ
    
    def Fonc_label_nbr_ligne_et_col(self, df, VarNbLigneCol):
        tx = f"rows : {df.shape[0]}  columns : {df.shape[1]}"
        VarNbLigneCol.set(tx)