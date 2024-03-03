# jav_pytools/os/tree.py

import os
import pyperclip

from jav_pytools.os._utils.headers import add_headers_to_files

# Importar la función para añadir headers desde headers.py
# Asegúrate de que la ruta de importación sea correcta según tu estructura de directorios

def main(set_headers=False, output_to_file=False):
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
            # Filtra los directorios a excluir en cada nivel del árbol
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(exclude_prefix)]

            level = root.replace(startpath, '').count(os.sep)
            structure = add_directory_structure(structure, root, level)

            sublevel = level + 1
            for f in sorted(files):
                structure = add_file_structure(structure, f, sublevel)
        return structure

    # Especifica aquí los directorios a excluir en cualquier nivel
    exclude_dirs = ["__pycache__", "venv", ".git", "tools", "archivos"]
    exclude_prefix = "venv"  # Si no hay prefijo específico a excluir, se deja vacío

    try:
        structure = list_files('.', exclude_dirs, exclude_prefix)

        # Lógica para manejar la salida basada en output_to_file
        if output_to_file:
            output_dir = "tools"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'estructura.txt')

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(structure)
            print(f"El archivo '{output_path}' ha sido generado correctamente.")
        else:
            pass
            # print(structure)  # Simplemente imprime la estructura en la consola

        pyperclip.copy(structure)
        print("La estructura del directorio ha sido copiada al portapapeles.")

        # Llamar a add_headers_to_files si set_headers es True
        if set_headers:
            add_headers_to_files()

    except OSError as e:
        print(f"Error al trabajar con el archivo: {e}")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Cambia True a False si no quieres añadir headers automáticamente
    # Cambia output_to_file a True si deseas que el resultado se escriba en un archivo
    main(set_headers=True, output_to_file=False)
