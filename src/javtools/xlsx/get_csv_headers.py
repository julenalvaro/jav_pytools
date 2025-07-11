import tkinter as tk
from tkinter import filedialog
import pyperclip
import pandas as pd
import os

def get_file_path():
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
    num_lines_str = input("¿Cuántas líneas quieres mostrar? (por defecto, 5): ").strip()
    return 5 if not num_lines_str else int(num_lines_str)

def load_dataframes(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".csv":
        df = pd.read_csv(file_path, nrows=None)
        sheet_name = os.path.basename(file_path)
        return {sheet_name: df}
    else:
        return pd.read_excel(file_path, sheet_name=None)

def copy_to_clipboard_and_print(dataframes, num_lines):
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
    return final_text

def ask_save_csv():
    save_csv_str = input("\n¿Quieres guardar estos datos en archivo(s) CSV? (s/n): ").strip().lower()
    return save_csv_str in ('s', 'si', 'y', 'yes')

def save_to_csv(file_path, dataframes, num_lines, clipboard_text):
    file_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = os.path.join(file_dir, f"{base_name}_csv_headers")
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
    
    headers_file_path = os.path.join(out_dir, f"{base_name}_headers.csv")
    try:
        with open(headers_file_path, "w", encoding="utf-8") as f:
            f.write(clipboard_text)
        print(f"Archivo de headers guardado en: {headers_file_path}")
    except Exception as e:
        print(f"No se pudo guardar el archivo de headers: {e}")

def main():
    file_path = get_file_path()
    if not file_path:
        print("No se ha seleccionado ningún archivo. Saliendo...")
        return
    num_lines = ask_num_lines()
    dataframes = load_dataframes(file_path)
    clipboard_text = copy_to_clipboard_and_print(dataframes, num_lines)
    if ask_save_csv():
        save_to_csv(file_path, dataframes, num_lines, clipboard_text)

if __name__ == "__main__":
    main()
