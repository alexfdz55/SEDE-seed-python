"""
Módulo central de validación de archivos Excel
Contiene la lógica compartida entre la versión CLI y Streamlit
"""

import pandas as pd
import warnings
from config import HOJAS_REQUERIDAS, COLUMNAS_REQUERIDAS
from validadores import VALIDADORES

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def construir_contexto(excel_file, archivo_excel):
    """
    Construye el diccionario de contexto con datos de referencia
    para validaciones cruzadas entre hojas.
    
    Args:
        excel_file: pd.ExcelFile objeto
        archivo_excel: ruta o archivo Excel
        
    Returns:
        dict: Diccionario con listas de valores válidos por categoría
    """
    contexto = {}
    
    # Sedes
    if "Sedes" in excel_file.sheet_names:
        df_sedes = pd.read_excel(archivo_excel, sheet_name="Sedes", header=1)
        col_nombre_sede = COLUMNAS_REQUERIDAS["Sedes"][0]
        if col_nombre_sede in df_sedes.columns:
            contexto['sedes'] = df_sedes[df_sedes[col_nombre_sede].notna()][col_nombre_sede].unique().tolist()
    
    # Cursos académicos
    if "Cursos académicos" in excel_file.sheet_names:
        df_cursos = pd.read_excel(archivo_excel, sheet_name="Cursos académicos", header=1)
        col_nombre_curso = COLUMNAS_REQUERIDAS["Cursos académicos"][0]
        if col_nombre_curso in df_cursos.columns:
            # Convertir a string para manejar tanto enteros como strings
            contexto['cursos_academicos'] = [str(int(c)) if isinstance(c, (int, float)) and not pd.isna(c) else str(c) 
                                             for c in df_cursos[df_cursos[col_nombre_curso].notna()][col_nombre_curso].unique().tolist()]
    
    # Grados
    if "Grados" in excel_file.sheet_names:
        df_grados = pd.read_excel(archivo_excel, sheet_name="Grados", header=1)
        col_nombre_grado = COLUMNAS_REQUERIDAS["Grados"][1]
        if col_nombre_grado in df_grados.columns:
            contexto['grados'] = [str(g) for g in df_grados[df_grados[col_nombre_grado].notna()][col_nombre_grado].unique().tolist()]
    
    # Áreas
    if "Áreas" in excel_file.sheet_names:
        df_areas = pd.read_excel(archivo_excel, sheet_name="Áreas", header=1)
        col_nombre_area = COLUMNAS_REQUERIDAS["Áreas"][0]
        if col_nombre_area in df_areas.columns:
            contexto['areas'] = df_areas[df_areas[col_nombre_area].notna()][col_nombre_area].unique().tolist()
    
    # Asignaturas
    if "Asignaturas" in excel_file.sheet_names:
        df_asignaturas = pd.read_excel(archivo_excel, sheet_name="Asignaturas", header=1)
        col_nombre_asignatura = COLUMNAS_REQUERIDAS["Asignaturas"][0]
        if col_nombre_asignatura in df_asignaturas.columns:
            contexto['asignaturas'] = df_asignaturas[df_asignaturas[col_nombre_asignatura].notna()][col_nombre_asignatura].unique().tolist()
    
    # Profesores
    if "Profesores" in excel_file.sheet_names:
        df_profesores = pd.read_excel(archivo_excel, sheet_name="Profesores", header=1)
        col_num_doc_profesor = COLUMNAS_REQUERIDAS["Profesores"][3]
        if col_num_doc_profesor in df_profesores.columns:
            contexto['profesores_docs'] = [str(d) for d in df_profesores[df_profesores[col_num_doc_profesor].notna()][col_num_doc_profesor].unique().tolist()]
    
    return contexto


def validar_hoja(nombre_hoja, df, contexto):
    """
    Valida una hoja individual.
    
    Args:
        nombre_hoja: Nombre de la hoja
        df: DataFrame con los datos
        contexto: Diccionario de contexto
        
    Returns:
        dict: Resultados de validación para la hoja
    """
    resultado = {
        'valido': True,
        'errores': [],
        'advertencias': []
    }
    
    # Validar contenido usando el validador específico
    if nombre_hoja in VALIDADORES:
        validador = VALIDADORES[nombre_hoja]
        
        try:
            # Intentar con contexto
            resultado = validador(df, nombre_hoja, contexto=contexto)
        except TypeError:
            # Validador antiguo sin contexto
            resultado = validador(df, nombre_hoja)
    
    return resultado
