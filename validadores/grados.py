import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_grados(df, nombre_hoja):
    """
    Valida la hoja Grados
    
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
    
    # Validar que haya al menos un grado
    if len(df) == 0:
        errores.append("Debe haber al menos un grado registrado")
    
    # Validar que los nombres de grado no estén duplicados
    if 'Nombre del grado' in df.columns:
        duplicados = df[df['Nombre del grado'].duplicated(keep=False)]
        if len(duplicados) > 0:
            errores.append(f"Hay {len(duplicados)} nombre(s) de grado duplicado(s)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
