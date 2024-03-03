# setup.py

from setuptools import setup, find_packages

# Usar with para asegurar que el archivo se cierre correctamente
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='javtools',
    version='0.1',
    packages=find_packages(),
    description='Herramientas personalizadas para mi uso.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Indicar el tipo de contenido del long_description
    install_requires=[
        'pyperclip==1.8.2', 
    ],
    entry_points={
        'console_scripts': [
            'jav-tree=jav_pytools.os.tree:main',
        ],
    },
)
