# src/os/add_root_to_path.py

# jav_pytools/os/add_root_to_path.py

# add_root_to_path.py
import os
import sys
from pathlib import Path

def find_git_root(path: Path) -> Path:
    """Busca de manera ascendente hasta encontrar un directorio .git."""
    if (path / '.git').exists():
        return path
    if path.parent == path:
        raise RuntimeError("No se encontró el directorio .git")
    return find_git_root(path.parent)

def add_root_to_path():
    project_root = find_git_root(Path(__file__).resolve())
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    # print(f"Raíz del proyecto añadida al sys.path: {project_root}")
