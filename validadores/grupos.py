import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_grupos(df, nombre_hoja, contexto=None):
    """
    Valida la hoja Grupos
    
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
    col_nombre = columnas[0]           # Nombre del grupo
    col_grado = columnas[1]            # Nombre del grado
    col_sedes = columnas[2]            # Sedes asociadas
    col_capacidad = columnas[3]        # Capacidad
    
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
    
    # Validar que no haya nombres de grupo duplicados
    if col_nombre in df.columns:
        duplicados = df[df[col_nombre].duplicated(keep=False) & df[col_nombre].notna()]
        if len(duplicados) > 0:
            nombres_dup = duplicados[col_nombre].unique()
            errores.append(f"Hay {len(duplicados)} nombre(s) de grupo duplicado(s): {', '.join(nombres_dup)}")
    
    # Validar que los grados asociados existan en la hoja Grados
    if contexto and 'grados' in contexto and col_grado in df.columns:
        grados_validos = contexto['grados']
        grados_asignados = df[df[col_grado].notna()][col_grado].unique()
        grados_invalidos = [grado for grado in grados_asignados if grado not in grados_validos]
        
        if grados_invalidos:
            errores.append(f"Hay {len(grados_invalidos)} grado(s) asignado(s) que no existen: {', '.join(grados_invalidos)}")
    
    # Validar que las sedes asociadas (separadas por coma) existan en la hoja Sedes
    if contexto and 'sedes' in contexto and col_sedes in df.columns:
        sedes_validas = contexto['sedes']
        sedes_invalidas_encontradas = set()
        
        for _, row in df.iterrows():
            if pd.notna(row[col_sedes]):
                # Separar por coma y limpiar espacios
                sedes_lista = [sede.strip() for sede in str(row[col_sedes]).split(',')]
                for sede in sedes_lista:
                    if sede and sede not in sedes_validas:
                        sedes_invalidas_encontradas.add(sede)
        
        if sedes_invalidas_encontradas:
            errores.append(f"Hay {len(sedes_invalidas_encontradas)} sede(s) asociada(s) que no existen: {', '.join(sorted(sedes_invalidas_encontradas))}")
    
    # Validar capacidad (debe ser número positivo)
    if col_capacidad in df.columns:
        capacidades_invalidas = df[df[col_capacidad].notna() & (df[col_capacidad] <= 0)]
        if len(capacidades_invalidas) > 0:
            errores.append(f"Hay {len(capacidades_invalidas)} grupo(s) con capacidad inválida (debe ser mayor a 0)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
