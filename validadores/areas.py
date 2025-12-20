import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_areas(df, nombre_hoja):
    """
    Valida la hoja Áreas
    
    Args:
        df: DataFrame con los datos de la hoja
        nombre_hoja: Nombre de la hoja
        
    Returns:
        dict: Resultado de la validación con 'valido', 'errores' y 'advertencias'
    """
    errores = []
    advertencias = []
    
    # Obtener nombres de columnas desde la configuración
    columnas = COLUMNAS_REQUERIDAS[nombre_hoja]
    col_nombre = columnas[0]  # Nombre del área
    
    # Validar que no esté vacía
    if df.empty:
        errores.append("La hoja está vacía")
        return {
            'valido': False,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que haya al menos una área
    if len(df) == 0:
        errores.append("Debe haber al menos un área registrada")
    
    # Validar que los nombres de área no estén duplicados
    if col_nombre in df.columns:
        duplicados = df[df[col_nombre].duplicated(keep=False) & df[col_nombre].notna()]
        if len(duplicados) > 0:
            nombres_dup = duplicados[col_nombre].unique()
            errores.append(f"Hay {len(duplicados)} nombre(s) de área duplicado(s): {', '.join(nombres_dup)}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
