import os
import re
from pathlib import Path

def is_target_file(filename, target_extensions, target_prefixes, target_exact_names):
    lower_name = filename.lower()
    extension = Path(filename).suffix
    if extension in target_extensions:
        return True
    if any(lower_name.startswith(pref) for pref in target_prefixes):
        return True
    if lower_name in {e.lower() for e in target_exact_names}:
        return True
    return False

def get_comment_token(extension, comment_tokens):
    return comment_tokens.get(extension, comment_tokens['default'])

def remove_old_paths(lines, comment_token):
    # Eliminamos cualquier línea que comience con el token de comentario y contenga "PATH:"
    pattern = re.compile(r'^\s*' + re.escape(comment_token) + r'\s*PATH:.*', re.IGNORECASE)
    return [line for line in lines if not pattern.match(line)]

def clean_extra_newlines(lines):
    """
    Garantiza que después del header haya exactamente DOS saltos de línea antes del contenido real.
    """
    # Eliminamos líneas en blanco después del header
    while len(lines) > 1 and lines[1].strip() == '':
        lines.pop(1)  
    
    # Agregamos exactamente DOS saltos de línea después del header
    lines.insert(1, "\n")
    return lines

def process_file(file_path, startpath, target_extensions, target_prefixes,
                 target_exact_names, comment_tokens, end_comment_tokens):
    # 1. Determinar extensión y token de comentario
    filename = file_path.name
    extension = file_path.suffix
    token = get_comment_token(extension, comment_tokens)

    # 2. Verificar si es archivo objetivo
    if not is_target_file(filename, target_extensions, target_prefixes, target_exact_names):
        return

    # 3. Determinar ruta relativa para el header
    relative_path = file_path.relative_to(startpath).as_posix()
    header_line = f"{token} PATH: {relative_path}"
    if extension in end_comment_tokens:
        header_line += end_comment_tokens[extension]
    header_line += "\n"

    # 4. Leer archivo y limpiar encabezados viejos
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = remove_old_paths(lines, token)
        new_lines.insert(0, header_line)
        new_lines = clean_extra_newlines(new_lines)

        # 5. Sobrescribir el archivo con el nuevo contenido limpio
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")

def add_headers_to_files(startpath, exclude_dirs):
    # Extensiones / nombres a procesar
    target_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.css', '.yml','.toml'}
    target_prefixes = {'.env'}
    target_exact_names = {'Dockerfile'}

    # Tokens de comentario
    comment_tokens = {
        '.py': '#',
        '.js': '//',
        '.jsx': '//',
        '.ts': '//',
        '.tsx': '//',
        '.css': '/*',
        '.yml': '#',
        '.toml': '#',
        'default': '#'
    }
    end_comment_tokens = {'.css': ' */'}

    for foldername, subfolders, filenames in os.walk(startpath):
        # Evitamos las carpetas excluidas
        if any(excl in foldername for excl in exclude_dirs):
            continue
        for filename in filenames:
            file_path = Path(foldername) / filename
            process_file(
                file_path=file_path,
                startpath=startpath,
                target_extensions=target_extensions,
                target_prefixes=target_prefixes,
                target_exact_names=target_exact_names,
                comment_tokens=comment_tokens,
                end_comment_tokens=end_comment_tokens
            )

    print("Headers actualizados correctamente.")
