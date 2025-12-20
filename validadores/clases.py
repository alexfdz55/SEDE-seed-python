import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_clases(df, nombre_hoja):
    """
    Valida la hoja Clases
    
    Args:
        df: DataFrame con los datos de la hoja
        nombre_hoja: Nombre de la hoja
        
    Returns:
        dict: Resultado de la validación con 'valido', 'errores' y 'advertencias'
    """
    errores = []
    advertencias = []
    
    # Validar que no esté vacía
    if df.empty:
        advertencias.append("La hoja está vacía (puede ser opcional)")
        return {
            'valido': True,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que no haya clases duplicadas (misma asignatura, grado, grupo, sede y año)
    columnas_clave = ['Nombre de la asignatura', 'Nombre del grado', 'Nombre del grupo', 
                      'Sede asociada', 'Año escolar asociado']
    
    if all(col in df.columns for col in columnas_clave):
        duplicados = df[df.duplicated(subset=columnas_clave, keep=False)]
        if len(duplicados) > 0:
            advertencias.append(f"Hay {len(duplicados)} clase(s) potencialmente duplicada(s)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
