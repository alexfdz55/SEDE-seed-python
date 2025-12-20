import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_asignaturas(df, nombre_hoja):
    """
    Valida la hoja Asignaturas
    
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
    
    # Validar que haya al menos una asignatura
    if len(df) == 0:
        errores.append("Debe haber al menos una asignatura registrada")
    
    # Validar que los nombres de asignatura no estén duplicados
    if 'Nombre de la asignatura' in df.columns:
        duplicados = df[df['Nombre de la asignatura'].duplicated(keep=False)]
        if len(duplicados) > 0:
            advertencias.append(f"Hay {len(duplicados)} nombre(s) de asignatura duplicado(s) (puede ser intencional)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
