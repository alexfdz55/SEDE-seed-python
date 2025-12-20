import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_sedes(df, nombre_hoja):
    """
    Valida la hoja Sedes
    
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
    
    # Validar que haya al menos una sede
    if len(df) == 0:
        errores.append("Debe haber al menos una sede registrada")
    
    # Validar que los correos tengan formato válido
    if 'Correo electrónico' in df.columns:
        correos_invalidos = df[df['Correo electrónico'].notna() & 
                              ~df['Correo electrónico'].str.contains('@', na=False)]
        if len(correos_invalidos) > 0:
            errores.append(f"Hay {len(correos_invalidos)} correo(s) con formato inválido")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
