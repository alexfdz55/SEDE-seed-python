import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_profesores(df, nombre_hoja, contexto=None):
    """
    Valida la hoja Profesores
    
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
    col_nombres = columnas[0]           # Nombres
    col_apellidos = columnas[1]         # Apellidos
    col_tipo_doc = columnas[2]          # Tipo de documento
    col_num_doc = columnas[3]           # Número de documento
    col_telefono = columnas[4]          # Teléfono
    col_direccion = columnas[5]         # Dirección
    col_correo = columnas[6]            # Correo electrónico
    col_sede = columnas[7]              # Sede asignada
    col_asignaturas = columnas[8]       # Asignaturas a cargo
    
    # Validar que no esté vacía
    if df.empty:
        advertencias.append("La hoja está vacía (puede ser opcional)")
        return {
            'valido': True,
            'errores': errores,
            'advertencias': advertencias
        }
    
    # Validar formato de correos electrónicos
    if col_correo in df.columns:
        correos_invalidos = df[df[col_correo].notna() & 
                              ~df[col_correo].str.contains('@', na=False)]
        if len(correos_invalidos) > 0:
            errores.append(f"Hay {len(correos_invalidos)} correo(s) con formato inválido")
    
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
    
    # Validar que no haya correos duplicados
    if col_correo in df.columns:
        duplicados = df[df[col_correo].duplicated(keep=False) & df[col_correo].notna()]
        if len(duplicados) > 0:
            correos_dup = duplicados[col_correo].unique()
            errores.append(f"Hay {len(duplicados)} correo(s) electrónico(s) duplicado(s): {', '.join(correos_dup)}")
    
    # Validar que las sedes asignadas existan en la hoja Sedes
    if contexto and 'sedes' in contexto and col_sede in df.columns:
        sedes_validas = contexto['sedes']
        sedes_asignadas = df[df[col_sede].notna()][col_sede].unique()
        sedes_invalidas = [sede for sede in sedes_asignadas if sede not in sedes_validas]
        
        if sedes_invalidas:
            errores.append(f"Hay {len(sedes_invalidas)} sede(s) asignada(s) que no existen: {', '.join(sedes_invalidas)}")
    
    # Validar que las asignaturas a cargo (separadas por coma) existan en la hoja Asignaturas
    if contexto and 'asignaturas' in contexto and col_asignaturas in df.columns:
        asignaturas_validas = contexto['asignaturas']
        asignaturas_invalidas_encontradas = set()
        
        for _, row in df.iterrows():
            if pd.notna(row[col_asignaturas]):
                # Separar por coma y limpiar espacios
                asignaturas_lista = [asig.strip() for asig in str(row[col_asignaturas]).split(',')]
                for asignatura in asignaturas_lista:
                    if asignatura and asignatura not in asignaturas_validas:
                        asignaturas_invalidas_encontradas.add(asignatura)
        
        if asignaturas_invalidas_encontradas:
            errores.append(f"Hay {len(asignaturas_invalidas_encontradas)} asignatura(s) a cargo que no existen: {', '.join(sorted(asignaturas_invalidas_encontradas))}")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
