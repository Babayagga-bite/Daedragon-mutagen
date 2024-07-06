#!/bin/bash

# Crear un entorno virtual
python3 -m venv venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install transformers torch datasets

# Ejecutar el script de Python
python3 daedragon_mutagen.py

# Desactivar el entorno virtual al finalizar
deactivate

