# tools/headers.py

import os
from pathlib import Path

def find_project_root(start_path: Path) -> Path:
    if (start_path / '.git').exists():
        return start_path
    
    if start_path.parent == start_path:
        return start_path
    
    return find_project_root(start_path.parent)

comment_tokens = {
    '.py': '#',
    '.js': '//',
}

target_extensions = ['.py', '.js']
exclude_dirs = ["venv"]  # Agregar cualquier otro directorio que quieras excluir

current_path = Path(__file__).parent
root_dir = find_project_root(current_path)

for foldername, subfolders, filenames in os.walk(root_dir):
    # Excluir directorios especificados
    if any(exclude_dir in foldername for exclude_dir in exclude_dirs):
        continue
    
    for filename in filenames:
        _, extension = os.path.splitext(filename)

        if extension in target_extensions:
            file_path = Path(foldername) / filename
            relative_path = file_path.relative_to(root_dir).as_posix()  # as_posix() convierte las rutas a formato POSIX

            try:
                with open(file_path, 'r') as file:
                    first_line = file.readline().strip()
                    if first_line == f"{comment_tokens[extension]} {relative_path}":
                        continue
            except Exception as e:
                print(f"Error al leer el archivo {file_path}: {str(e)}")
                continue

            try:
                with open(file_path, 'r') as file:
                    content = file.read()

                with open(file_path, 'w') as file:
                    file.write(f"{comment_tokens[extension]} {relative_path}\n\n{content}")
            except Exception as e:
                print(f"Error al escribir en el archivo {file_path}: {str(e)}")

print(f"Headers añadidos para archivos {', '.join(target_extensions)}.")
