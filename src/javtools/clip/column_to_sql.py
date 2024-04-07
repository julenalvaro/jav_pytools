# PATH: src/javtools/clip/column_to_sql.py

import pyperclip
import re

def buscar_ordenes_excel():
    # Obtener el contenido del portapapeles
    clipboard_content = pyperclip.paste()

    # Utilizar expresiones regulares para buscar órdenes en formato de columna de Excel
    # Suponemos que las órdenes están en una columna y separadas por líneas
    ordenes = re.findall(r'\b\d+\b', clipboard_content)

    if ordenes:
        # Generar la lista de órdenes para la consulta SQL
        lista_ordenes_sql = ', '.join([f"'{orden}'" for orden in ordenes])

        # Agregar paréntesis alrededor de la lista de órdenes
        lista_ordenes_sql = f"({lista_ordenes_sql})"

        # Copiar la lista de órdenes al portapapeles
        pyperclip.copy(lista_ordenes_sql)

        print("La lista de órdenes ha sido copiada al portapapeles con paréntesis.")
    else:
        print("No se encontraron órdenes en formato de columna de Excel en el portapapeles.")

if __name__ == "__main__":
    buscar_ordenes_excel()
