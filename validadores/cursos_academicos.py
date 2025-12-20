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
    
    # Obtener nombres de columnas desde la configuración
    columnas = COLUMNAS_REQUERIDAS[nombre_hoja]
    col_nombre = columnas[0]        # Nombre del año escolar
    col_fecha_inicio = columnas[1]  # Fecha de inicio
    col_fecha_fin = columnas[2]     # Fecha fin
    
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
    
    # Validar que no haya nombres de año escolar duplicados
    if col_nombre in df.columns:
        duplicados = df[df[col_nombre].duplicated(keep=False) & df[col_nombre].notna()]
        if len(duplicados) > 0:
            nombres_dup = duplicados[col_nombre].unique()
            errores.append(f"Hay {len(duplicados)} nombre(s) de año escolar duplicado(s): {', '.join(nombres_dup)}")
    
    # Validar que las fechas sean válidas
    if col_fecha_inicio in df.columns and col_fecha_fin in df.columns:
        try:
            # Intentar convertir a datetime
            df[col_fecha_inicio] = pd.to_datetime(df[col_fecha_inicio], errors='coerce')
            df[col_fecha_fin] = pd.to_datetime(df[col_fecha_fin], errors='coerce')
            
            # Verificar fechas nulas (no válidas)
            fechas_inicio_invalidas = df[df[col_fecha_inicio].isna()]
            if len(fechas_inicio_invalidas) > 0:
                errores.append(f"Hay {len(fechas_inicio_invalidas)} fecha(s) de inicio inválida(s)")
            
            fechas_fin_invalidas = df[df[col_fecha_fin].isna()]
            if len(fechas_fin_invalidas) > 0:
                errores.append(f"Hay {len(fechas_fin_invalidas)} fecha(s) de fin inválida(s)")
            
            # Validar que fecha fin sea mayor que fecha inicio
            fechas_logicas_invalidas = df[(df[col_fecha_inicio].notna()) & 
                                          (df[col_fecha_fin].notna()) & 
                                          (df[col_fecha_fin] <= df[col_fecha_inicio])]
            if len(fechas_logicas_invalidas) > 0:
                errores.append(f"Hay {len(fechas_logicas_invalidas)} curso(s) con fecha fin menor o igual a fecha inicio")
        except Exception as e:
            advertencias.append(f"No se pudieron validar completamente las fechas: {str(e)}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
