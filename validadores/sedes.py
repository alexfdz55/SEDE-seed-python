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
    
    # Obtener nombres de columnas desde la configuración
    columnas = COLUMNAS_REQUERIDAS[nombre_hoja]
    col_nombre = columnas[0]      # Nombre de la institución
    col_direccion = columnas[1]   # Dirección
    col_telefono = columnas[2]    # Teléfono
    col_correo = columnas[3]      # Correo electrónico
    col_dane = columnas[4]        # Código Dane
    
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
    if col_correo in df.columns:
        correos_invalidos = df[df[col_correo].notna() & 
                              ~df[col_correo].str.contains('@', na=False)]
        if len(correos_invalidos) > 0:
            errores.append(f"Hay {len(correos_invalidos)} correo(s) con formato inválido")
    
    # Validar que no haya nombres de institución duplicados
    if col_nombre in df.columns:
        duplicados = df[df[col_nombre].duplicated(keep=False) & df[col_nombre].notna()]
        if len(duplicados) > 0:
            nombres_dup = duplicados[col_nombre].unique()
            errores.append(f"Hay {len(duplicados)} nombre(s) de institución duplicado(s): {', '.join(nombres_dup)}")
    
    # Validar que no haya teléfonos duplicados
    if col_telefono in df.columns:
        duplicados = df[df[col_telefono].duplicated(keep=False) & df[col_telefono].notna()]
        if len(duplicados) > 0:
            telefonos_dup = duplicados[col_telefono].unique()
            # No es un error bloqueante: los teléfonos pueden repetirse entre sedes
            advertencias.append(
                f"⚠️ Hay {len(duplicados)} teléfono(s) duplicado(s): {', '.join(map(str, telefonos_dup))}"
            )
    
    # Validar que no haya correos duplicados
    if col_correo in df.columns:
        duplicados = df[df[col_correo].duplicated(keep=False) & df[col_correo].notna()]
        if len(duplicados) > 0:
            correos_dup = duplicados[col_correo].unique()
            # No es un error bloqueante: los correos pueden repetirse entre sedes
            advertencias.append(
                f"⚠️ Hay {len(duplicados)} correo(s) electrónico(s) duplicado(s): {', '.join(correos_dup)}"
            )
    
    # Validar que no haya códigos Dane duplicados
    if col_dane in df.columns:
        duplicados = df[df[col_dane].duplicated(keep=False) & df[col_dane].notna()]
        if len(duplicados) > 0:
            codigos_dup = duplicados[col_dane].unique()
            errores.append(f"Hay {len(duplicados)} código(s) Dane duplicado(s): {', '.join(map(str, codigos_dup))}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
