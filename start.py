#!/usr/bin/env python3
"""
Script de inicio para Railway que maneja correctamente las variables de entorno.
"""
import os
import sys
import subprocess

# Obtener el puerto de Railway (si existe) o usar 8501 por defecto
port = os.environ.get('PORT', '8501')

# IMPORTANTE: Eliminar STREAMLIT_SERVER_PORT si Railway la inyectó incorrectamente
if 'STREAMLIT_SERVER_PORT' in os.environ:
    del os.environ['STREAMLIT_SERVER_PORT']

# Configurar las variables de entorno correctas
os.environ['STREAMLIT_SERVER_PORT'] = port
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Ejecutar Streamlit
cmd = ['streamlit', 'run', 'app_streamlit.py']
sys.exit(subprocess.call(cmd))
