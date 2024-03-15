# PATH: src/javtools/os/recycle_bin.py

from pathlib import Path
from datetime import datetime, timedelta

def cutoff_recycle_bin(directory_path, days_old):
    # Convierte el directorio a un objeto Path para facilitar la manipulación
    dir_path = Path(directory_path)
    
    # Calcula la fecha de corte
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    # Verifica cada archivo en el directorio
    for item in dir_path.iterdir():
        if item.is_file():  # Asegura que sea un archivo y no un directorio
            # Compara la fecha de modificación del archivo con la fecha de corte
            mod_time = datetime.fromtimestamp(item.stat().st_mtime)
            if mod_time < cutoff_date:
                try:
                    item.unlink()  # Elimina el archivo
                    print(f"Archivo eliminado: {item}")
                except Exception as e:
                    print(f"No se pudo eliminar el archivo {item}: {e}")
        elif item.is_dir():  # Si es un directorio, podrías llamar recursivamente a recycle_bin
            # Opcional: Llamar a recycle_bin(item, days_old) para hacerlo recursivo
            pass