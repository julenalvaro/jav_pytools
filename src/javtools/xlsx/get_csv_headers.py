# PATH: src/javtools/xlsx/get_csv_headers.py

import tkinter as tk
from tkinter import filedialog
import pyperclip
import pandas as pd
import os

def main():
    """
    Abre un cuadro de diálogo para seleccionar un archivo .csv, .xlsx o .xlsm.
    Pregunta cuántas líneas se quieren mostrar (por defecto, 10).
    Recorre todas las hojas del documento y copia al portapapeles
    una línea por hoja con el nombre de la hoja y sus columnas separadas por ';'.
    Muestra también por consola los primeros N registros de cada hoja.
    """
    # Inicializa la ventana de Tkinter (sin que aparezca la ventana principal)
    root = tk.Tk()
    root.withdraw()

    # Abre el explorador de archivos para escoger el CSV/XLSX/XLSM
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo CSV, XLSX o XLSM",
        filetypes=[
            ("Todos los archivos", "*.*")
            ("Archivos CSV", "*.csv"),
            ("Archivos Excel", "*.xlsx *.xlsm"),
        ]
    )

    if not file_path:
        print("No se ha seleccionado ningún archivo. Saliendo...")
        return

    # Pregunta cuántas líneas mostrar (por defecto, 10)
    num_lines_str = input("¿Cuántas líneas quieres mostrar? (por defecto, 10): ").strip()
    num_lines = 10 if not num_lines_str else int(num_lines_str)

    # Dependiendo de la extensión, leemos el archivo de distinta forma
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Diccionario: key=nombre de hoja, value=DataFrame
    dataframes = {}

    if file_ext == ".csv":
        # Cuando es CSV, técnicamente solo hay 1 "hoja"
        df = pd.read_csv(file_path, nrows=None)  # leemos todo para los headers
        sheet_name = os.path.basename(file_path)  # usar nombre de archivo como "nombre de hoja"
        dataframes[sheet_name] = df
    else:
        # Para XLSX o XLSM, leemos todas las hojas
        dataframes = pd.read_excel(file_path, sheet_name=None)

    # Vamos a construir el texto que irá al portapapeles
    # Una línea por cada hoja, en formato: "NombreHoja;col1;col2;col3..."
    lines_for_clipboard = []

    for sheet_name, df in dataframes.items():
        # Mostramos por consola los primeros N registros
        print(f"\n=== Hoja: {sheet_name} ===")
        print(df.head(num_lines).to_string(index=False))

        # Tomamos las columnas, las unimos con ';'
        columns_joined = ";".join(str(col) for col in df.columns)
        # Nombre de la hoja + las columnas
        line = f"{sheet_name};{columns_joined}"
        lines_for_clipboard.append(line)

    # Unimos todo con saltos de línea
    final_text = "\n".join(lines_for_clipboard)
    # Lo copiamos al portapapeles
    pyperclip.copy(final_text)

    print("\nLos headers se han copiado al portapapeles.")
    print("Formato: una línea por hoja, con el nombre de la hoja y sus columnas separados por ';'.")

if __name__ == "__main__":
    main()
