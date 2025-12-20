import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_profesores(df, nombre_hoja):
    """
    Valida la hoja Profesores
    
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
    
    # Validar correos electrónicos
    if 'Correo electrónico' in df.columns:
        correos_invalidos = df[df['Correo electrónico'].notna() & 
                              ~df['Correo electrónico'].str.contains('@', na=False)]
        if len(correos_invalidos) > 0:
            errores.append(f"Hay {len(correos_invalidos)} correo(s) con formato inválido")
    
    # Validar duplicados de documento
    if 'Número de documento' in df.columns:
        duplicados = df[df['Número de documento'].duplicated(keep=False)]
        if len(duplicados) > 0:
            errores.append(f"Hay {len(duplicados)} número(s) de documento duplicado(s)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
