import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_periodos(df, nombre_hoja, contexto=None):
    """
    Valida la hoja Periodos
    
    Args:
        df: DataFrame con los datos de la hoja
        nombre_hoja: Nombre de la hoja
        contexto: Diccionario con datos de otras hojas (opcional)
        
    Returns:
        dict: Resultado de la validación con 'valido', 'errores' y 'advertencias'
    """
    errores = []
    advertencias = []
    
    # Obtener nombres de columnas desde la configuración
    columnas = COLUMNAS_REQUERIDAS[nombre_hoja]
    col_nombre = columnas[0]           # Nombre del periodo
    col_fecha_inicio = columnas[1]     # Fecha de inicio
    col_fecha_fin = columnas[2]        # Fecha fin
    col_curso = columnas[3]            # Año escolar asociado
    
    # Validar que no esté vacía
    if df.empty:
        errores.append("La hoja está vacía")
        return {
            'valido': False,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que haya al menos un periodo
    if len(df) == 0:
        errores.append("Debe haber al menos un periodo registrado")
    
    # Validar que no haya nombres de periodo duplicados dentro del mismo curso
    if col_nombre in df.columns:
        if col_curso in df.columns:
            # Considerar duplicados sólo cuando nombre y curso coinciden
            mask = df[col_nombre].notna() & df[col_curso].notna()
            df_valid = df[mask]
            duplicados = df_valid[df_valid.duplicated(subset=[col_curso, col_nombre], keep=False)]
            if len(duplicados) > 0:
                combos = duplicados[[col_nombre, col_curso]].drop_duplicates()
                combos_list = [f"{r[col_nombre]} ({r[col_curso]})" for _, r in combos.iterrows()]
                errores.append(
                    f"Hay {len(duplicados)} periodo(s) duplicado(s) dentro del mismo curso: {', '.join(combos_list)}"
                )
        else:
            # Sin columna de curso, usar comportamiento anterior (global)
            duplicados = df[df[col_nombre].duplicated(keep=False) & df[col_nombre].notna()]
            if len(duplicados) > 0:
                nombres_dup = duplicados[col_nombre].unique()
                errores.append(f"Hay {len(duplicados)} nombre(s) de periodo duplicado(s): {', '.join(nombres_dup)}")
    
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
                errores.append(f"Hay {len(fechas_logicas_invalidas)} periodo(s) con fecha fin menor o igual a fecha inicio")
        except Exception as e:
            advertencias.append(f"No se pudieron validar completamente las fechas: {str(e)}")
    
    # Validar que los años escolares asociados existan en Cursos académicos
    if contexto and 'cursos_academicos' in contexto and col_curso in df.columns:
        cursos_validos = contexto['cursos_academicos']
        cursos_asociados = df[df[col_curso].notna()][col_curso].unique()
        cursos_invalidos = [curso for curso in cursos_asociados if curso not in cursos_validos]
        
        if cursos_invalidos:
            errores.append(f"Hay {len(cursos_invalidos)} año(s) escolar(es) asociado(s) que no existen: {', '.join(cursos_invalidos)}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
