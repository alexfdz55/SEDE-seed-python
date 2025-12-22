#!/usr/bin/env python3
"""
Script de inicio para Railway que maneja correctamente las variables de entorno.
"""
import os
import sys

# Obtener el puerto de Railway (si existe) o usar 8501 por defecto
port = os.environ.get('PORT', '8501')

# CRÍTICO: Forzar eliminación de variables problemáticas
env_vars_to_remove = ['STREAMLIT_SERVER_PORT', 'STREAMLIT_SERVER_ADDRESS']
for var in env_vars_to_remove:
    os.environ.pop(var, None)

# Configurar argumentos de línea de comandos ANTES de importar streamlit
sys.argv = [
    'streamlit',
    'run',
    'app_streamlit.py',
    f'--server.port={port}',
    '--server.address=0.0.0.0',
    '--server.headless=true',
    '--browser.gatherUsageStats=false'
]

# Importar y ejecutar Streamlit
from streamlit.web import cli as stcli

if __name__ == '__main__':
    sys.exit(stcli.main())
