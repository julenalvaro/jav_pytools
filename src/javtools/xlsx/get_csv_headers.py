# PATH: src/javtools/xlsx/get_csv_headers.py

import tkinter as tk
from tkinter import filedialog
import pyperclip
import pandas as pd
import os

def get_file_path():
    """
    Abre un cuadro de diálogo para seleccionar un archivo .csv, .xlsx o .xlsm.
    Retorna la ruta seleccionada o una cadena vacía si no seleccionaste nada.
    """
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Selecciona un archivo CSV, XLSX o XLSM",
        filetypes=[
            ("Todos los archivos", "*.*"),
            ("Archivos CSV", "*.csv"),
            ("Archivos Excel", "*.xlsx *.xlsm"),
        ]
    )

def ask_num_lines():
    """
    Pregunta cuántas líneas se desean mostrar y retorna un entero (por defecto, 5).
    """
    num_lines_str = input("¿Cuántas líneas quieres mostrar? (por defecto, 5): ").strip()
    return 5 if not num_lines_str else int(num_lines_str)

def load_dataframes(file_path):
    """
    Carga y retorna un diccionario con {nombre_de_hoja: DataFrame}.
    Si el archivo es CSV, se asume una sola 'hoja' usando el nombre del archivo.
    """
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".csv":
        df = pd.read_csv(file_path, nrows=None)
        sheet_name = os.path.basename(file_path)
        return {sheet_name: df}
    else:
        return pd.read_excel(file_path, sheet_name=None)

def copy_to_clipboard_and_print(dataframes, num_lines):
    """
    Muestra en consola y copia al portapapeles las primeras N filas de cada hoja
    en formato CSV separado por ';'.
    """
    lines_for_clipboard = []
    for sheet_name, df in dataframes.items():
        df_head = df.head(num_lines)
        csv_text = df_head.to_csv(index=False, sep=';')
        print(f"\n=== Hoja: {sheet_name} ===")
        print(csv_text)
        lines_for_clipboard.append(f"=== Hoja: {sheet_name} ===\n{csv_text}")
    final_text = "\n".join(lines_for_clipboard)
    pyperclip.copy(final_text)
    print("\nLas primeras líneas se han copiado al portapapeles en formato CSV separado por ';'.")

def ask_save_csv():
    """
    Pregunta si se desea guardar los datos en archivos CSV. Retorna True/False.
    """
    save_csv_str = input("\n¿Quieres guardar estos datos en archivo(s) CSV? (s/n): ").strip().lower()
    return save_csv_str in ('s', 'si', 'y', 'yes')

def save_to_csv(file_path, dataframes, num_lines):
    """
    Genera un CSV por cada hoja en un subdirectorio {nombre_archivo}_csv_headers,
    guardando las primeras N filas. Intenta sobreescribir los existentes.
    Ante cualquier problema, muestra el error pero no interrumpe el flujo.
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = f"{base_name}_csv_headers"
    os.makedirs(out_dir, exist_ok=True)
    for sheet_name, df in dataframes.items():
        try:
            df_head = df.head(num_lines)
            safe_sheet_name = (sheet_name
                                .replace('/', '_')
                                .replace('\\', '_')
                                .replace(':', '_'))
            out_path = os.path.join(out_dir, f"{safe_sheet_name}.csv")
            df_head.to_csv(out_path, index=False, sep=';')
            print(f"Archivo CSV generado: {out_path}")
        except Exception as e:
            print(f"No se pudo generar el archivo CSV para la hoja '{sheet_name}': {e}")

def main():
    file_path = get_file_path()
    if not file_path:
        print("No se ha seleccionado ningún archivo. Saliendo...")
        return
    num_lines = ask_num_lines()
    dataframes = load_dataframes(file_path)
    copy_to_clipboard_and_print(dataframes, num_lines)
    if ask_save_csv():
        save_to_csv(file_path, dataframes, num_lines)

if __name__ == "__main__":
    main()
