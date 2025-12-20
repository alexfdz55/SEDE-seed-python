import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_grupos(df, nombre_hoja):
    """
    Valida la hoja Grupos
    
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
    
    # Validar que haya al menos un grupo
    if len(df) == 0:
        errores.append("Debe haber al menos un grupo registrado")
    
    # Validar capacidad (debe ser número positivo)
    if 'Capacidad' in df.columns:
        capacidades_invalidas = df[df['Capacidad'].notna() & (df['Capacidad'] <= 0)]
        if len(capacidades_invalidas) > 0:
            errores.append(f"Hay {len(capacidades_invalidas)} grupo(s) con capacidad inválida (debe ser mayor a 0)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
