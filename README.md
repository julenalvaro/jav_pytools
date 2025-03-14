# jav-pytools

Herramientas personalizadas para mi uso en proyectos Python.

## Instalación

Para instalar este paquete en modo editable, usa:
```bash
pip install --editable .
```
Esto permitirá modificar el código sin necesidad de reinstalar el paquete cada vez.

## Uso de los comandos

Este paquete registra comandos ejecutables en la terminal usando **entry points** en `setup.py`. Esto permite ejecutar comandos personalizados como `jav-tree` y `jav-csv` desde cualquier terminal.

### Ejecutar comandos

```bash
jav-tree
```
```bash
jav-csv
```
Si el comando no es reconocido, sigue los pasos de depuración en la sección siguiente.

## Depuración de problemas con los entry points

Si un comando no funciona, sigue estos pasos:

### 1️⃣ Verifica si el comando está registrado
Ejecuta:
```bash
python -c "import pkg_resources; print([ep for ep in pkg_resources.iter_entry_points('console_scripts')])"
```
Si el comando no aparece en la lista, es probable que no esté bien definido en `setup.py`.

### 2️⃣ Verifica que el módulo se pueda importar
Ejecuta:
```bash
python -c "import javtools.xlsx.get_csv_headers; print(javtools.xlsx.get_csv_headers)"
```
Si da error, revisa que `__init__.py` exista en todas las carpetas necesarias.

### 3️⃣ Reinstala en modo editable
```bash
pip uninstall javtools -y
pip install --editable .
```
Después, verifica los entry points nuevamente:
```bash
python -c "import pkg_resources; print([ep for ep in pkg_resources.iter_entry_points('console_scripts')])"
```

### 4️⃣ Verifica si el comando está en el PATH
En Windows:
```powershell
where jav-csv
```
Si no aparece, agrégalo manualmente al PATH:
```powershell
setx PATH "%USERPROFILE%\AppData\Local\Programs\Python\Scripts;%PATH%"
```
Reinicia la terminal y prueba de nuevo.

En Linux/Mac:
```bash
which jav-csv
```
Si no está en el PATH, agrégalo con:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 5️⃣ Fuerza la regeneración de scripts ejecutables
Si todo lo anterior falla:
```bash
pip uninstall javtools -y
pip install --editable .
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```
Esto mostrará la carpeta donde se instalaron los scripts. Entra ahí y revisa si `jav-csv` está presente.

## Conclusión
Si `jav-csv` no aparece en los entry points, revisa `setup.py` (especialmente `find_packages()`). Si `jav-csv` aparece en los entry points pero no funciona, es un problema del `PATH` en tu sistema.

Prueba estos pasos y verifica que todo esté correctamente configurado.

