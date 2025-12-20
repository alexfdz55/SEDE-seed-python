import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_asignaturas(df, nombre_hoja, contexto=None):
    """
    Valida la hoja Asignaturas
    
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
    col_nombre = columnas[0]        # Nombre de la asignatura
    col_area = columnas[1]          # Área asociada
    col_grados = columnas[2]        # Grados asociados
    
    # Validar que no esté vacía
    if df.empty:
        errores.append("La hoja está vacía")
        return {
            'valido': False,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que haya al menos una asignatura
    if len(df) == 0:
        errores.append("Debe haber al menos una asignatura registrada")
    
    # Validar que los nombres de asignatura no estén duplicados
    if col_nombre in df.columns:
        duplicados = df[df[col_nombre].duplicated(keep=False) & df[col_nombre].notna()]
        if len(duplicados) > 0:
            nombres_dup = duplicados[col_nombre].unique()
            errores.append(f"Hay {len(duplicados)} nombre(s) de asignatura duplicado(s): {', '.join(nombres_dup)}")
    
    # Validar que las áreas asociadas existan en la hoja Áreas
    if contexto and 'areas' in contexto and col_area in df.columns:
        areas_validas = contexto['areas']
        areas_asignadas = df[df[col_area].notna()][col_area].unique()
        areas_invalidas = [area for area in areas_asignadas if area not in areas_validas]
        
        if areas_invalidas:
            errores.append(f"Hay {len(areas_invalidas)} área(s) asociada(s) que no existen: {', '.join(areas_invalidas)}")
    
    # Validar que los grados asociados (separados por coma) existan en la hoja Grados
    if contexto and 'grados' in contexto and col_grados in df.columns:
        grados_validos = contexto['grados']
        grados_invalidos_encontrados = set()
        
        for _, row in df.iterrows():
            if pd.notna(row[col_grados]):
                # Separar por coma y limpiar espacios
                grados_lista = [grado.strip() for grado in str(row[col_grados]).split(',')]
                for grado in grados_lista:
                    if grado and grado not in grados_validos:
                        grados_invalidos_encontrados.add(grado)
        
        if grados_invalidos_encontrados:
            errores.append(f"Hay {len(grados_invalidos_encontrados)} grado(s) asociado(s) que no existen: {', '.join(sorted(grados_invalidos_encontrados))}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
