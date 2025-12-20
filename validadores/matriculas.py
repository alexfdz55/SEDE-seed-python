import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_matriculas(df, nombre_hoja):
    """
    Valida la hoja Matrículas
    
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
    
    # Validar correos electrónicos del estudiante
    if 'Correo electrónico' in df.columns:
        correos_invalidos = df[df['Correo electrónico'].notna() & 
                              ~df['Correo electrónico'].str.contains('@', na=False)]
        if len(correos_invalidos) > 0:
            advertencias.append(f"Hay {len(correos_invalidos)} correo(s) de estudiante con formato inválido")
    
    # Validar duplicados de documento
    if 'Número de documento' in df.columns:
        duplicados = df[df['Número de documento'].duplicated(keep=False)]
        if len(duplicados) > 0:
            errores.append(f"Hay {len(duplicados)} número(s) de documento duplicado(s)")
    
    # Validar que las fechas de nacimiento sean coherentes
    if 'Fecha de nacimiento' in df.columns:
        try:
            df['Fecha de nacimiento'] = pd.to_datetime(df['Fecha de nacimiento'], errors='coerce')
            fechas_futuras = df[df['Fecha de nacimiento'] > pd.Timestamp.now()]
            if len(fechas_futuras) > 0:
                errores.append(f"Hay {len(fechas_futuras)} estudiante(s) con fecha de nacimiento futura")
        except:
            advertencias.append("No se pudieron validar las fechas de nacimiento")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
