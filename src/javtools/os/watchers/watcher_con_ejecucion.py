# PATH: src/javtools/watchers/watcher_con_ejecucion.py

import re
import json
from pathlib import Path
from datetime import datetime

def watch_and_execute(dir_watch, file_watch_regex, last_run_metadata_file, funcion_externa):
    try:
        with open(last_run_metadata_file, 'r') as file:
            last_run_metadata = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        last_run_metadata = {}

    watch_dir = Path(dir_watch)
    regex_pattern = file_watch_regex

    latest_file = None
    latest_mod_time = None
    for file in watch_dir.glob('*'):
        if re.search(regex_pattern, file.name):
            mod_time = file.stat().st_mtime
            if latest_file is None or mod_time > latest_mod_time:
                latest_file = file
                latest_mod_time = mod_time

    if latest_file is None:
        return None

    file_metadata = {'path': str(latest_file), 'mod_time': latest_mod_time}
    if file_metadata != last_run_metadata.get('latest_file'):
        try:
            # Intenta ejecutar la función externa con la ruta del archivo más reciente
            funcion_externa(str(latest_file))
            # Si la ejecución fue exitosa, actualiza los metadatos
            with open(last_run_metadata_file, 'w') as file:
                json.dump({'latest_file': file_metadata}, file)
            return str(latest_file)
        except Exception as e:
            # Maneja cualquier error que ocurra durante la ejecución de la función externa
            print(f"Error durante la ejecución de la función externa: {e}")
            # Decide no actualizar los metadatos debido al fallo
            return None

    return None
