import os
from pathlib import Path
import re

def add_headers_to_files(startpath, exclude_dirs):
    # 1. Configuración general
    target_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.css', '.yml'}  # Archivos por extensión
    target_prefixes = {'.env'}  # Archivos que empiezan con un prefijo
    target_exact_names = {'Dockerfile'}  # Archivos con nombre exacto (case-insensitive)

    # 2. Tokens de comentarios
    comment_tokens = {
        '.py': '#', 
        '.js': '//', 
        '.jsx': '//', 
        '.ts': '//', 
        '.tsx': '//', 
        '.css': '/*',
        '.yml': '#',
        'default': '#'  # Para archivos sin extensión (ej. Dockerfile, .env)
    }
    
    end_comment_tokens = {'.css': ' */'}  # Token de fin de comentario para CSS

    for foldername, subfolders, filenames in os.walk(startpath):
        if any(exclude_dir in foldername for exclude_dir in exclude_dirs):
            continue

        for filename in filenames:
            file_path = Path(foldername) / filename
            relative_path = file_path.relative_to(startpath).as_posix()
            lower_filename = filename.lower()
            file_extension = Path(filename).suffix

            # 3. Detectar si el archivo es objetivo
            if file_extension in target_extensions:
                header_token = comment_tokens.get(file_extension, '#')
            elif any(lower_filename.startswith(prefix) for prefix in target_prefixes):
                header_token = comment_tokens['default']
            elif lower_filename in {name.lower() for name in target_exact_names}:
                header_token = comment_tokens['default']
            else:
                continue  # No es un archivo objetivo

            # 4. Patrón regex para detectar si el header ya existe
            header_pattern = re.compile(r'^\s*' + re.escape(header_token) + r' PATH: ' + re.escape(relative_path) + r'\s*$')

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                # 5. Identificar si el header ya existe
                header_exists = any(header_pattern.match(line) for line in lines)

                if header_exists:
                    continue  # Si ya existe, no hacer nada

                # 6. Eliminar encabezados viejos o líneas vacías iniciales
                new_lines = [line for line in lines if not header_pattern.match(line)]
                
                # 7. Insertar nuevo header
                header = f"{header_token} PATH: {relative_path}"
                if file_extension in end_comment_tokens:
                    header += end_comment_tokens[file_extension]
                header += "\n\n"

                new_lines.insert(0, header)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(new_lines)

            except Exception as e:
                print(f"Error al procesar {file_path}: {e}")

    print("Headers actualizados correctamente.")

