import pandas as pd
from config import COLUMNAS_REQUERIDAS

def validar_calificaciones_anuales(df, nombre_hoja, contexto=None):
    """
    Valida la hoja Calificaciones anuales
    
    Args:
        df: DataFrame con los datos de la hoja
        nombre_hoja: Nombre de la hoja
        contexto: Diccionario con datos de referencia de otras hojas
        
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
    
    # Obtener nombres de columnas desde configuración
    columnas = COLUMNAS_REQUERIDAS[nombre_hoja]
    col_num_doc = columnas[0]      # Número de documento del estudiante
    col_nombre = columnas[1]        # Nombre del estudiante
    col_asignatura = columnas[2]    # Nombre de la asignatura
    col_año_escolar = columnas[3]   # Año escolar
    col_sede = columnas[4]          # Sede asignada
    col_tipo_nota = columnas[5]     # Tipo de nota
    col_promedio = columnas[6]      # Promedio anual
    col_aprobo = columnas[7]        # Aprobó
    
    # 1. Validar año escolar
    if contexto and 'cursos_academicos' in contexto and col_año_escolar in df.columns:
        cursos_validos = contexto['cursos_academicos']
        años_invalidos = set()
        
        for _, row in df.iterrows():
            if pd.notna(row[col_año_escolar]):
                # Convertir a string sin decimales si es número
                año = str(int(row[col_año_escolar])) if isinstance(row[col_año_escolar], (int, float)) else str(row[col_año_escolar]).strip()
                if año and año not in cursos_validos:
                    años_invalidos.add(año)
        
        if años_invalidos:
            errores.append(f"Hay {len(años_invalidos)} año(s) escolar(es) que no existen: {', '.join(sorted(años_invalidos))}")
    
    # 2. Validar sede asignada
    if contexto and 'sedes' in contexto and col_sede in df.columns:
        sedes_validas = contexto['sedes']
        sedes_invalidas = set()
        
        for _, row in df.iterrows():
            if pd.notna(row[col_sede]):
                sede = str(row[col_sede]).strip()
                if sede and sede not in sedes_validas:
                    sedes_invalidas.add(sede)
        
        if sedes_invalidas:
            errores.append(f"Hay {len(sedes_invalidas)} sede(s) asignada(s) que no existen: {', '.join(sorted(sedes_invalidas))}")
    
    # 3. Validar tipo de nota (enum)
    TIPOS_NOTA_VALIDOS = ["Cualitativa (Letras)", "Cuantitativa (Números)"]
    
    if col_tipo_nota in df.columns:
        tipos_invalidos = df[df[col_tipo_nota].notna() & 
                            ~df[col_tipo_nota].isin(TIPOS_NOTA_VALIDOS)]
        if len(tipos_invalidos) > 0:
            valores_unicos = tipos_invalidos[col_tipo_nota].unique()
            errores.append(
                f"Hay {len(tipos_invalidos)} registro(s) con tipo de nota inválido. "
                f"Valores encontrados: {', '.join(map(str, valores_unicos))}"
            )
    
    # 4. Validar promedio anual (solo para notas cuantitativas)
    if col_tipo_nota in df.columns and col_promedio in df.columns:
        df_cuantitativa = df[df[col_tipo_nota] == "Cuantitativa (Números)"]
        
        if not df_cuantitativa.empty:
            try:
                # Convertir a numérico
                promedios = pd.to_numeric(df_cuantitativa[col_promedio], errors='coerce')
                
                # Verificar valores no numéricos
                no_numericos = df_cuantitativa[promedios.isna() & 
                                              df_cuantitativa[col_promedio].notna()]
                if len(no_numericos) > 0:
                    errores.append(
                        f"Hay {len(no_numericos)} registro(s) cuantitativos con promedio no numérico"
                    )
                
                # Verificar rango 0-5
                df_cuantitativa_valid = df_cuantitativa.copy()
                df_cuantitativa_valid['promedio_num'] = promedios
                fuera_rango = df_cuantitativa_valid[
                    (df_cuantitativa_valid['promedio_num'].notna()) &
                    ((df_cuantitativa_valid['promedio_num'] < 0) | 
                     (df_cuantitativa_valid['promedio_num'] > 5))
                ]
                if len(fuera_rango) > 0:
                    errores.append(
                        f"Hay {len(fuera_rango)} promedio(s) fuera del rango válido (0-5)"
                    )
            except Exception as e:
                advertencias.append(f"No se pudieron validar completamente los promedios: {str(e)}")
    
    # 5. Validar asignatura con reporte estadístico detallado (solo advertencia)
    if contexto and 'asignaturas' in contexto and col_asignatura in df.columns:
        asignaturas_validas = contexto['asignaturas']
        
        # Filtrar registros con asignaturas inválidas
        registros_invalidos = df[df[col_asignatura].notna() & 
                                ~df[col_asignatura].isin(asignaturas_validas)]
        
        if not registros_invalidos.empty:
            total_records = len(df[df[col_asignatura].notna()])
            count_invalid_records = len(registros_invalidos)
            percentage = (count_invalid_records / total_records) * 100 if total_records > 0 else 0
            
            # Obtener TODAS las asignaturas inválidas únicas
            asignaturas_invalidas = sorted(registros_invalidos[col_asignatura].unique())
            count_unique = len(asignaturas_invalidas)
            
            warning_msg = (
                f"⚠️ Hay {count_invalid_records} registro(s) ({percentage:.1f}%) con asignaturas inválidas. "
                f"{count_unique} asignatura(s) única(s) no existen: {', '.join(asignaturas_invalidas)}. "
                f"Estos registros serán omitidos en la exportación."
            )
            
            advertencias.append(warning_msg)
    
    # 6. Mostrar todos los tipos únicos de "Promedio anual"
    if col_promedio in df.columns:
        tipos_promedio = df[df[col_promedio].notna()][col_promedio].unique()
        if len(tipos_promedio) > 0:
            advertencias.append(
                f"Tipos encontrados en '{col_promedio}': {', '.join(map(str, sorted(tipos_promedio)))}"
            )
    
    # 7. Mostrar todos los tipos únicos de "Aprobó"
    if col_aprobo in df.columns:
        tipos_aprobo = df[df[col_aprobo].notna()][col_aprobo].unique()
        if len(tipos_aprobo) > 0:
            advertencias.append(
                f"Valores encontrados en '{col_aprobo}': {', '.join(map(str, sorted(tipos_aprobo)))}"
            )
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias
    }
