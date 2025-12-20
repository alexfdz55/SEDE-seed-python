import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_cursos_academicos(df, nombre_hoja):
    """
    Valida la hoja Cursos académicos
    
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
    
    # Validar que haya al menos un curso académico
    if len(df) == 0:
        errores.append("Debe haber al menos un curso académico registrado")
    
    # Validar fechas (que fecha fin sea mayor que fecha inicio)
    if 'Fecha de inicio' in df.columns and 'Fecha fin' in df.columns:
        try:
            df['Fecha de inicio'] = pd.to_datetime(df['Fecha de inicio'], errors='coerce')
            df['Fecha fin'] = pd.to_datetime(df['Fecha fin'], errors='coerce')
            
            fechas_invalidas = df[df['Fecha fin'] <= df['Fecha de inicio']]
            if len(fechas_invalidas) > 0:
                errores.append(f"Hay {len(fechas_invalidas)} curso(s) con fecha fin menor o igual a fecha inicio")
        except:
            advertencias.append("No se pudieron validar las fechas")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
