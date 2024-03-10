# src/os/_utils/headers.py

import os
from pathlib import Path

def add_headers_to_files(startpath):
    
    comment_tokens = {'.py': '#', '.js': '//'}
    target_extensions = ['.py', '.js']
    exclude_dirs = ["venv"]

    current_path = Path(__file__).parent

    for foldername, subfolders, filenames in os.walk(startpath):
        # Excluir directorios especificados
        if any(exclude_dir in foldername for exclude_dir in exclude_dirs):
            continue
        
        for filename in filenames:
            _, extension = os.path.splitext(filename)

            if extension in target_extensions:
                file_path = Path(foldername) / filename
                relative_path = file_path.relative_to(startpath).as_posix()  # as_posix() convierte las rutas a formato POSIX

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:  # Añade encoding='utf-8'
                        first_line = file.readline().strip()
                        if first_line == f"{comment_tokens[extension]} {relative_path}":
                            continue
                except Exception as e:
                    print(f"Error al leer el archivo {file_path}: {str(e)}")
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:  # Añade encoding='utf-8'
                        content = file.read()

                    with open(file_path, 'w', encoding='utf-8') as file:  # Añade encoding='utf-8' aquí también
                        file.write(f"{comment_tokens[extension]} {relative_path}\n\n{content}")
                except Exception as e:
                    print(f"Error al escribir en el archivo {file_path}: {str(e)}")


    print(f"Headers añadidos para archivos {', '.join(target_extensions)}.")
