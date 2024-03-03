import os
import pyperclip

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
    for root, dirs, files in os.walk(startpath):
        # Ajustamos la exclusión para que sea exacta, no parcial
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in [os.path.join(startpath, ed) for ed in exclude_dirs]]
        dirs[:] = [d for d in dirs if not d.startswith(exclude_prefix)]

        level = root.replace(startpath, '').count(os.sep)
        structure = add_directory_structure(structure, root, level)

        sublevel = level + 1
        for f in sorted(files):
            structure = add_file_structure(structure, f, sublevel)
    return structure

# Modifica esto para incluir las carpetas que quieras excluir de forma exacta
exclude_dirs = [".git", "__pycache__", ".vscode", "tools", "archivos"]
# Ahora se espera una coincidencia exacta de la ruta
exclude_prefix = "venv"

try:
    output_dir = "tools"
    os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta tools si no existe
    output_path = os.path.join(output_dir, 'estructura.txt')
    
    # Escribe la estructura del directorio en el archivo 'tools/estructura.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        structure = list_files('.', exclude_dirs, exclude_prefix)  # Genera la estructura del directorio
        f.write(structure)

    # Copia la estructura del directorio al portapapeles
    pyperclip.copy(structure)
    
    # Imprime un mensaje de éxito
    print(f"El archivo '{output_path}' ha sido generado correctamente y su contenido ha sido copiado en el portapapeles")

except OSError as e:
    print(f"Error al trabajar con el archivo: {e}")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
