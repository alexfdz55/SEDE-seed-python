import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_calificaciones_anuales(df, nombre_hoja):
    """
    Valida la hoja Calificaciones anuales
    
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
    
    # Validar que el promedio anual sea un número válido
    if 'Promedio anual' in df.columns:
        try:
            promedios_invalidos = df[df['Promedio anual'].notna() & 
                                    ((df['Promedio anual'] < 0) | (df['Promedio anual'] > 5))]
            if len(promedios_invalidos) > 0:
                errores.append(f"Hay {len(promedios_invalidos)} promedio(s) fuera del rango válido (0-5)")
        except:
            advertencias.append("No se pudieron validar los promedios")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
