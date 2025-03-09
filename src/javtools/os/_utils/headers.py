# PATH: src/javtools/os/_utils/headers.py

import os
from pathlib import Path
import re

def add_headers_to_files(startpath, exclude_dirs):
    # 1. Definir parámetros configurables
    target_extensions = {'.py', '.js', '.jsx', '.css', '.yml'}  # Archivos por extensión
    target_prefixes = {'.env'}  # Archivos que empiezan con un prefijo
    target_exact_names = {'Dockerfile'}  # Archivos con nombre exacto (case-insensitive)

    # 2. Definir tokens de comentario
    comment_tokens = {
        '.py': '#', 
        '.js': '//', 
        '.jsx': '//', 
        '.css': '/*',
        '.yml': '#',
        'default': '#'  # Para archivos sin extensión (ej. Dockerfile, .env)
    }
    
    end_comment_tokens = {'.css': ' */'}  # Token de fin de comentario para CSS

    # 3. Crear patrones de regex para detectar headers existentes
    path_comment_patterns = {
        ext: re.compile(r'^\s*' + re.escape(comment_tokens.get(ext, '#')) + r' PATH: .+?$')
        for ext in target_extensions
    }

    for foldername, subfolders, filenames in os.walk(startpath):
        if any(exclude_dir in foldername for exclude_dir in exclude_dirs):
            continue

        for filename in filenames:
            file_path = Path(foldername) / filename
            relative_path = file_path.relative_to(startpath).as_posix()

            # 4. Identificar archivos objetivo
            file_extension = Path(filename).suffix
            lower_filename = filename.lower()

            if file_extension in target_extensions:
                header_token = comment_tokens.get(file_extension, '#')
            elif any(lower_filename.startswith(prefix) for prefix in target_prefixes):
                header_token = comment_tokens['default']
            elif lower_filename in {name.lower() for name in target_exact_names}:
                header_token = comment_tokens['default']
            else:
                continue  # No es un archivo objetivo, se omite

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                # 5. Identificar el índice donde terminan los headers y líneas vacías al inicio
                end_of_header_index = 0
                for line in lines:
                    if path_comment_patterns.get(file_extension, re.compile(r'^$')).match(line) or line.strip() == '':
                        end_of_header_index += 1
                    else:
                        break

                # 6. Eliminar comentarios de ruta y líneas vacías al inicio
                new_lines = lines[end_of_header_index:]

                # 7. Insertar el nuevo comentario de ruta al inicio
                header = f"{header_token} PATH: {relative_path}"
                if file_extension in end_comment_tokens:
                    header += end_comment_tokens[file_extension]
                header += "\n\n"
                new_lines.insert(0, header)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(new_lines)

            except Exception as e:
                print(f"Error al procesar el archivo {file_path}: {str(e)}")

    print(f"Headers y líneas vacías actualizados correctamente para los archivos configurados.")





