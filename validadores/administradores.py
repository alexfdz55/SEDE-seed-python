import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_administradores(df, nombre_hoja):
    """
    Valida la hoja Administradores
    
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
    col_nombres = columnas[0]        # Nombres
    col_apellidos = columnas[1]      # Apellidos
    col_correo = columnas[2]         # Correo electrónico
    col_tipo_doc = columnas[3]       # Tipo de documento
    col_num_doc = columnas[4]        # Número de documento
    col_telefono = columnas[5]       # Teléfono
    
    # Validar que no esté vacía
    if df.empty:
        errores.append("La hoja está vacía")
        return {
            'valido': False,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar que haya al menos un administrador
    if len(df) == 0:
        errores.append("Debe haber al menos un administrador registrado")
    
    # Validar formato de correos electrónicos
    if col_correo in df.columns:
        correos_invalidos = df[df[col_correo].notna() & 
                              ~df[col_correo].str.contains('@', na=False)]
        if len(correos_invalidos) > 0:
            errores.append(f"Hay {len(correos_invalidos)} correo(s) con formato inválido")
    
    # Validar que no haya correos duplicados
    if col_correo in df.columns:
        duplicados = df[df[col_correo].duplicated(keep=False) & df[col_correo].notna()]
        if len(duplicados) > 0:
            correos_dup = duplicados[col_correo].unique()
            errores.append(f"Hay {len(duplicados)} correo(s) electrónico(s) duplicado(s): {', '.join(correos_dup)}")
    
    # Validar que no haya números de documento duplicados
    if col_num_doc in df.columns:
        duplicados = df[df[col_num_doc].duplicated(keep=False) & df[col_num_doc].notna()]
        if len(duplicados) > 0:
            documentos_dup = duplicados[col_num_doc].unique()
            errores.append(f"Hay {len(duplicados)} número(s) de documento duplicado(s): {', '.join(map(str, documentos_dup))}")
    
    # Validar que no haya teléfonos duplicados
    if col_telefono in df.columns:
        duplicados = df[df[col_telefono].duplicated(keep=False) & df[col_telefono].notna()]
        if len(duplicados) > 0:
            telefonos_dup = duplicados[col_telefono].unique()
            errores.append(f"Hay {len(duplicados)} teléfono(s) duplicado(s): {', '.join(map(str, telefonos_dup))}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
