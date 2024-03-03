# Herramientas de Desarrollo - Scripts

## `headers.py`

### Descripción

El script `headers.py` está diseñado para añadir automáticamente comentarios de encabezado a los archivos de código fuente en el proyecto. Este comentario de encabezado incluye la ruta relativa del archivo desde la raíz del proyecto, lo que facilita la identificación del archivo cuando se trabaja con múltiples archivos abiertos o en revisiones de código.

### Uso

Para ejecutar el script, simplemente navega a la carpeta que contiene `headers.py` y ejecútalo con Python:

```bash
python headers.py
```

### Detalles de Implementación

El script recorre todos los archivos en el directorio del proyecto y sus subdirectorios, identificando los archivos de código fuente basándose en su extensión. Las extensiones predeterminadas que busca son .py y .js, pero esto se puede ajustar modificando la variable target_extensions en el script.

Para cada archivo de código fuente encontrado, el script añadirá (o actualizará si ya existe) un comentario en la primera línea del archivo con la ruta relativa del archivo desde la raíz del proyecto. Los comentarios son añadidos usando el token de comentario apropiado para el tipo de archivo (por ejemplo, # para archivos Python y // para archivos JavaScript).

### Configuración
Puedes ajustar el comportamiento del script modificando las siguientes variables al inicio del script:

- `comment_tokens`: Un diccionario que mapea las extensiones de archivo a los tokens de comentario correspondientes.
- `target_extensions:` Una lista de las extensiones de archivo que el script debe procesar.
- `exclude_dirs:` Una lista de nombres de directorios que el script debe ignorar durante la búsqueda de archivos.

### Requisitos

- Python 3.6 o superior

## `tree.py`

### Descripción

`tree.py` es un script diseñado para generar y listar la estructura de directorios del proyecto, excluyendo directorios específicos definidos por el usuario. El resultado se guarda en un archivo `estructura.txt` y también se copia al portapapeles para un acceso rápido.

### Uso

Para utilizar el script, ejecútalo directamente desde la línea de comandos en la raíz del proyecto:

```bash
python tools/tree.py
```

Una vez ejecutado, el script creará (o sobrescribirá si ya existe) un archivo llamado estructura.txt en la raíz del proyecto, que contendrá la estructura de directorios. Además, esta estructura será copiada al portapapeles.

### Configuración
Puedes personalizar los directorios que serán excluidos de la estructura modificando la lista exclude_dirs al inicio del script. Por defecto, esta lista incluye directorios comunes que suelen ser excluidos, como "venv", ".git", entre otros.

### Requisitos
El script requiere Python 3.6 o superior y la biblioteca pyperclip. Asegúrate de tener instalada esta última ejecutando:

```bash
pip install pyperclip
```