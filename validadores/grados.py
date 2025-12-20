import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_grados(df, nombre_hoja):
    """
    Valida la hoja Grados
    
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
    col_nivel = columnas[0]              # Nivel
    col_nombre = columnas[1]             # Nombre del grado
    col_tipo = columnas[2]               # Tipo de grado
    col_culminante = columnas[3]         # ¿Último grado culminante?
    
    # Tipos de grado válidos
    TIPOS_VALIDOS = [
        'EDUCACION_PREESCOLAR',
        'EDUCACION_BASICA_PRIMARIA',
        'EDUCACION_BASICA_SECUNDARIA',
        'EDUCACION_MEDIA'
    ]
    
    # Valores booleanos válidos
    VALORES_BOOLEANOS = ['Sí', 'No']
    
    # Validar que no esté vacía
    if df.empty:
        errores.append("La hoja está vacía")
        return {
            'valido': False,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que haya al menos un grado
    if len(df) == 0:
        errores.append("Debe haber al menos un grado registrado")
    
    # Validar que la combinación Nivel + Nombre del grado sea única
    if col_nivel in df.columns and col_nombre in df.columns:
        duplicados = df[df.duplicated(subset=[col_nivel, col_nombre], keep=False) & 
                       df[col_nivel].notna() & df[col_nombre].notna()]
        if len(duplicados) > 0:
            combinaciones_dup = duplicados[[col_nivel, col_nombre]].drop_duplicates()
            descripciones = [f"{row[col_nivel]} - {row[col_nombre]}" for _, row in combinaciones_dup.iterrows()]
            errores.append(f"Hay {len(duplicados)} combinación(es) Nivel-Nombre duplicada(s): {', '.join(descripciones)}")
    
    # Validar que el tipo de grado sea válido
    if col_tipo in df.columns:
        tipos_invalidos = df[df[col_tipo].notna() & ~df[col_tipo].isin(TIPOS_VALIDOS)]
        if len(tipos_invalidos) > 0:
            tipos_encontrados = tipos_invalidos[col_tipo].unique()
            errores.append(f"Hay {len(tipos_invalidos)} tipo(s) de grado inválido(s): {', '.join(tipos_encontrados)}. Valores permitidos: {', '.join(TIPOS_VALIDOS)}")
    
    # Validar que el campo culminante sea booleano (Sí o No)
    if col_culminante in df.columns:
        valores_invalidos = df[df[col_culminante].notna() & ~df[col_culminante].isin(VALORES_BOOLEANOS)]
        if len(valores_invalidos) > 0:
            valores_encontrados = valores_invalidos[col_culminante].unique()
            errores.append(f"Hay {len(valores_invalidos)} valor(es) inválido(s) en '¿Último grado culminante?': {', '.join(map(str, valores_encontrados))}. Solo se permite: Sí o No")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
