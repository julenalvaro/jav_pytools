# PATH: src/javtools/os/watchers/watcher_archivo.py

import re
import json
from pathlib import Path
from datetime import datetime

def watch_archivo(dir_watch, file_watch_regex, last_run_metadata_file):
    # Intenta cargar los metadatos; si falla, usa un diccionario vacío
    try:
        with open(last_run_metadata_file, 'r') as file:
            try:
                last_run_metadata = json.load(file)
            except json.JSONDecodeError:  # Captura el error si el archivo está vacío o malformado
                last_run_metadata = {}  # Usa un diccionario vacío como metadatos predeterminados
    except FileNotFoundError:
        last_run_metadata = {}  # También proporciona un diccionario vacío si el archivo no existe

    # Extrae la información necesaria de los argumentos proporcionados
    watch_dir = Path(dir_watch)
    regex_pattern = file_watch_regex

    # Encuentra el archivo más reciente que cumpla con la regex
    latest_file = None
    latest_mod_time = None
    for file in watch_dir.glob('*'):
        if re.search(regex_pattern, file.name):
            mod_time = file.stat().st_mtime
            if latest_file is None or mod_time > latest_mod_time:
                latest_file = file
                latest_mod_time = mod_time

    if latest_file is None:
        # No se encontró ningún archivo que cumpla con la condición
        return None

    # Compara los metadatos del archivo más reciente con los almacenados
    file_metadata = {'path': str(latest_file), 'mod_time': latest_mod_time}
    if file_metadata != last_run_metadata.get('latest_file'):
        # Si los metadatos no coinciden, actualiza el archivo de metadatos y retorna la ruta del archivo
        with open(last_run_metadata_file, 'w') as file:
            json.dump({'latest_file': file_metadata}, file)
        return str(latest_file)

    # Si los metadatos coinciden, no se ha detectado cambio en el archivo
    return None

# # Ejemplo de uso
# Definir los parámetros para la vigilancia
# dir_watch = './mi_directorio_a_vigilar'  # Ruta del directorio a vigilar
# file_watch_regex = r'reporte_.*\.txt'  # Expresión regular para identificar los archivos de interés
# last_run_metadata_file = './ultimo_metadato.txt'  # Ruta al archivo donde se guardarán los metadatos

# # Llamar a la función watcher_archivo con los parámetros definidos
# archivo_modificado = watcher_archivo(dir_watch, file_watch_regex, last_run_metadata_file)

# # Evaluar el resultado y actuar en consecuencia
# if archivo_modificado:
#     print(f"Se detectó un cambio en el archivo: {archivo_modificado}")
#     # Aquí podrías llamar a otra función que procese el archivo modificado, por ejemplo:
#     # procesar_archivo(archivo_modificado)
# else:
#     print("No se detectaron cambios en los archivos de interés.")

