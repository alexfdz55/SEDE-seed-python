# Sistema de Validación de Datos - Seed Pablo Neruda

Sistema completo de validación para archivos Excel de semilla de base de datos educativa. Incluye validaciones automáticas y análisis interactivo con Jupyter Notebook.

## 📋 Características

- ✅ **3 interfaces de uso**: CLI, Jupyter Notebook, y Web (Streamlit)
- ✅ Validación automatizada de 15 hojas de Excel
- ✅ Validación de integridad referencial entre hojas
- ✅ Detección de duplicados y valores inválidos
- ✅ Interfaz web interactiva con carga de archivos y dashboard
- ✅ Análisis interactivo con Jupyter Notebook
- ✅ Exportación de reportes de errores (CSV y TXT)
- ✅ Visualizaciones gráficas de errores con Plotly
- ✅ Arquitectura modular con código compartido
- ✅ Preparado para deployment (Docker, Railway, Dokploy)

## 🚀 Instalación

### Prerrequisitos

- Python 3.12 o superior (recomendado 3.12)
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Colocar archivo Excel**
   
   Coloca tu archivo Excel con nombre `Seed Pablo Neruda.xlsx` en la raíz del proyecto.

## 📖 Uso

### Opción 1: Validación por consola (Rápida)

Ejecuta el script de validación automática:

```bash
python analisis.py
```

Este script validará todas las hojas del Excel y mostrará un resumen de errores y advertencias.

**Ejemplo de salida:**
```
✓ El archivo Excel es VÁLIDO
Total de errores: 0
Total de advertencias: 2
```

### Opción 2: Análisis interactivo con Jupyter Notebook (Detallado)

Para explorar datos, ver gráficos y análisis detallados:

1. **Iniciar Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Abrir el notebook:**
   - En el navegador que se abre, haz clic en `analisis_excel.ipynb`

3. **Ejecutar el análisis:**
   - Ejecuta todas las celdas: `Cell > Run All`
   - O ejecuta celda por celda: `Shift + Enter`

### Opción 3: Interfaz Web con Streamlit (Interactiva y Visual)

Para usar la interfaz web con carga de archivos y visualizaciones interactivas:

1. **Iniciar la aplicación:**
   ```bash
   streamlit run app_streamlit.py
   ```

2. **Usar la interfaz:**
   - Abre tu navegador en `http://localhost:8501`
   - Arrastra y suelta tu archivo Excel o usa el botón de carga
   - Ve el progreso en tiempo real
   - Explora el dashboard con métricas y gráficos interactivos
   - Descarga reportes en CSV o TXT

**Ventajas:**
- ✨ No necesitas renombrar el archivo Excel
- 📊 Dashboard visual con métricas y gráficos
- ⚡ Progreso en tiempo real
- 💾 Descarga de reportes con un clic
- 🎨 Interfaz moderna y fácil de usar

### Reportes generados

Los reportes de errores se guardan automáticamente en la carpeta `reportes/`:

- `errores_asignaturas_invalidas.csv` - Lista detallada de registros con errores
- `lista_asignaturas_invalidas.txt` - Resumen de asignaturas inválidas

## 📁 Estructura del proyecto

```
seed-python/
├── analisis.py                    # Script CLI de validación
├── analisis_refactorizado.py     # Script CLI refactorizado (usa validador_core)
├── app_streamlit.py              # Aplicación web con Streamlit
├── validador_core.py             # Lógica de validación compartida
├── config.py                      # Configuración de hojas y columnas
├── analisis_excel.ipynb          # Notebook interactivo de análisis
├── requirements.txt              # Dependencias del proyecto
├── Dockerfile                     # Configuración Docker para deployment
├── Procfile                       # Configuración para Railway/Heroku
├── DEPLOYMENT.md                  # Guía de deployment
├── .streamlit/
│   └── config.toml               # Configuración de Streamlit
├── validadores/                  # Validadores modulares por hoja
│   ├── __init__.py
│   ├── sedes.py
│   ├── administradores.py
│   ├── coordinadores.py
│   ├── cursos_academicos.py
│   ├── periodos.py
│   ├── grados.py
│   ├── grupos.py
│   ├── areas.py
│   ├── asignaturas.py
│   ├── profesores.py
│   └── calificaciones_anuales.py
└── reportes/                     # Carpeta de reportes (generada automáticamente)
    ├── errores_asignaturas_invalidas.csv
    └── lista_asignaturas_invalidas.txt
```

## 🔍 Validaciones implementadas

### Por hoja:

1. **Sede principal** - Validación de estructura
2. **Sedes** - Unicidad de nombre, teléfono, correo, código Dane
3. **Administradores** - Unicidad de correo, documento, teléfono; formato email
4. **Coordinadores** - Unicidad y referencias a Sedes
5. **Cursos académicos** - Unicidad y validación de fechas
6. **Periodos** - Validación de fechas y referencia a Cursos académicos
7. **Grados** - Unicidad de nivel+nombre, tipos válidos
8. **Grupos** - Referencias a Grados y Sedes
9. **Áreas** - Unicidad de nombres
10. **Asignaturas** - Referencias a Áreas y Grados
11. **Profesores** - Unicidad y referencias a Sedes y Asignaturas
12. **Clases** - Validación de estructura
13. **Matrículas** - Validación de estructura
14. **Calificaciones anuales** - Referencias cruzadas, tipos de nota, rangos de promedios

### Validaciones cruzadas:

- Integridad referencial entre hojas
- Validación de listas separadas por comas
- Detección de valores inválidos con estadísticas detalladas

## 🛠️ Configuración

### Modificar columnas requeridas

Edita el archivo `config.py` para cambiar las columnas esperadas en cada hoja.

### Agregar nuevos validadores

1. Crea un archivo en `validadores/nuevo_validador.py`
2. Implementa la función `validar_nombre_hoja(df, nombre_hoja, contexto=None)`
3. Registra el validador en `validadores/__init__.py`

## 📊 Análisis con Jupyter Notebook

El notebook incluye:

- 📋 Vista general de todas las hojas con conteo de filas
- 🔍 Exploración detallada de columnas y tipos de datos
- 📈 Análisis de errores con estadísticas
- 📊 Gráficos de distribución de errores (barras, pie charts)
- 💾 Exportación automática de reportes

## 🚀 Deployment

La aplicación web está lista para deployment en múltiples plataformas:

### Railway (Recomendado)
- Deployment automático desde Git
- Plan gratuito disponible
- Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas

### Dokploy (Self-hosted)
- Deploy en tu propio servidor
- Control completo
- Incluye Dockerfile

### Streamlit Cloud
- Hosting gratuito para apps públicas
- Deploy con un clic desde GitHub

**Configuración incluida:**
- ✅ `Dockerfile` - Imagen Docker con Python 3.12
- ✅ `Procfile` - Configuración para Railway/Heroku
- ✅ `.streamlit/config.toml` - Configuración de la app
- ✅ Documentación completa en [DEPLOYMENT.md](DEPLOYMENT.md)

## 🤝 Contribuir

Para agregar nuevas validaciones:

1. No usar strings mágicos - usa `COLUMNAS_REQUERIDAS` de `config.py`
2. Seguir el patrón de validadores existentes
3. Retornar diccionario: `{'valido': bool, 'errores': list, 'advertencias': list}`
4. Documentar con docstrings

## 📝 Notas

- El archivo Excel no se sube a Git (`.gitignore`)
- Los reportes no se suben a Git (carpeta `reportes/`)
- El entorno virtual no se sube a Git (carpeta `venv/`)

## 📄 Licencia

Proyecto interno - INSTITUCIÓN EDUCATIVA PABLO NERUDA

---

**Desarrollado para la gestión de datos educativos** 🎓
