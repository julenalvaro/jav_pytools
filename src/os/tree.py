# src/os/tree.py

import os
import pyperclip

from src.os._utils.headers import add_headers_to_files

def generate_tree():
    def list_files(startpath, exclude_dirs, exclude_prefix):
        def add_directory_structure(structure, root, level):
            if level > 0:  # Esto asegura que no añadimos la raíz dos veces
                indent = '│   ' * (level - 1) + '├── '
                structure += indent + os.path.basename(root) + '/\n'
            return structure

        def add_file_structure(structure, file, level):
            indent = '│   ' * level + '├── '
            structure += indent + file + '\n'
            return structure

        structure = "./\n"  # Añade la raíz al inicio
        for root, dirs, files in os.walk(startpath, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(exclude_prefix)]
            level = root.replace(startpath, '').count(os.sep)
            structure = add_directory_structure(structure, root, level)
            sublevel = level + 1
            for f in sorted(files):
                structure = add_file_structure(structure, f, sublevel)
        return structure

    exclude_dirs = ["__pycache__", "venv", ".git", "tools", "archivos"]
    exclude_prefix = "venv"

    try:
        structure = list_files('.', exclude_dirs, exclude_prefix)
        pyperclip.copy(structure)
        print("La estructura del directorio ha sido copiada al portapapeles.")
        add_headers_to_files('.')  # Siempre añade headers
    except OSError as e:
        print(f"Error al trabajar con el archivo: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    generate_tree()
