# PATH: src/javtools/os/_utils/headers.py

import os
from pathlib import Path
import re

import os
from pathlib import Path
import re

def add_headers_to_files(startpath, exclude_dirs):
    # Tokens de comentarios para diferentes extensiones de archivo
    comment_tokens = {'.py': '#', 
                      '.js': '//', 
                      '.jsx': '//', 
                      '.css': '/*',
                      '.yml': '#',
                      'Dockerfile': '#'}
    
    end_comment_tokens = {'.css': ' */'}  # Token de fin de comentario para CSS

    target_extensions = [ '.py', 
                          '.js', 
                          '.jsx', 
                          '.css',
                          '.yml',
                          'Dockerfile']

    # Compilación de la expresión regular para la detección de comentarios de ruta en diferentes formatos
    path_comment_patterns = {
        ext: re.compile(r'^\s*' + re.escape(comment_tokens[ext]) + r' PATH: .+?$')
        for ext in target_extensions if ext in comment_tokens
    }

    for foldername, subfolders, filenames in os.walk(startpath):
        if any(exclude_dir in foldername for exclude_dir in exclude_dirs):
            continue

        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension in target_extensions:
                file_path = Path(foldername) / filename
                relative_path = file_path.relative_to(startpath).as_posix()

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    
                    # Identifica el índice donde terminan los comentarios de ruta y/o líneas vacías al inicio
                    end_of_header_index = 0
                    for line in lines:
                        if path_comment_patterns.get(extension, re.compile(r'^$')).match(line) or line.strip() == '':
                            end_of_header_index += 1
                        else:
                            break
                    
                    # Elimina los comentarios de ruta y líneas vacías al inicio
                    new_lines = lines[end_of_header_index:]
                    
                    # Inserta el nuevo comentario de ruta al inicio
                    header = f"{comment_tokens[extension]} PATH: {relative_path}"
                    if extension in end_comment_tokens:
                        header += end_comment_tokens[extension]
                    header += "\n\n"
                    new_lines.insert(0, header)

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(new_lines)

                except Exception as e:
                    print(f"Error al procesar el archivo {file_path}: {str(e)}")

    print(f"Headers y líneas vacías actualizados correctamente para archivos {', '.join(target_extensions)}.")



