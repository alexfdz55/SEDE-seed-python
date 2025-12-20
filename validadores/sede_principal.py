import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_sede_principal(df, nombre_hoja):
    """
    Valida la hoja Sede principal
    
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
        errores.append("La hoja está vacía")
        return {
            'valido': False,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que tenga al menos una fila de datos
    if len(df) == 0:
        errores.append("No hay datos en la hoja")
    
    # Aquí puedes agregar más validaciones específicas
    # Por ejemplo: validar formato de datos, valores obligatorios, etc.
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
