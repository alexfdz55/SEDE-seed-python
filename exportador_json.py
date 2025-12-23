"""
Exportador de Excel a formato JSON compatible con ModularSchoolConfig
"""
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any


class ExcelToJSONExporter:
    """Convierte un archivo Excel validado a formato JSON para el backend"""
    
    def __init__(self, excel_file: pd.ExcelFile):
        self.excel_file = excel_file
        
    def export_all(self) -> Dict[str, Any]:
        """
        Exporta todas las hojas a JSONs separados
        
        Returns:
            Dict con 4 keys: 'config', 'profesores', 'estudiantes', 'calificaciones_anuales'
        """
        return {
            'config': self.export_config(),
            'profesores': self.export_profesores(),
            'estudiantes': self.export_estudiantes(),
            'calificaciones_anuales': self.export_calificaciones()
        }
    
    def export_config(self) -> Dict[str, Any]:
        """Exporta la configuración principal de la escuela"""
        config = {
            'school': self._export_sede_principal(),
            'academicCourses': self._export_cursos_academicos(),
            'sessionTypes': self._get_default_session_types(),
            'levelingRule': self._get_default_leveling_rule(),
            'grades': self._export_grados(),
            'enrichedGrades': self._export_enriched_grades(),
            'classesDefaultCapacity': 30,
            'campuses': self._export_sedes(),
            'classes': self._export_grupos(),
            'subjects': self._export_asignaturas(),
            'areas': self._export_areas(),
            'admins': self._export_administradores(),
            'coordinators': self._export_coordinadores()
        }
        return config
    
    def _export_sede_principal(self) -> Dict[str, Any]:
        """Exporta datos de la sede principal"""
        if 'Sede principal' not in self.excel_file.sheet_names:
            return self._get_default_school()
        
        df = self.excel_file.parse('Sede principal', header=1)
        if df.empty:
            return self._get_default_school()
        
        row = df.iloc[0]
        return {
            'name': str(row.get('Nombre de la institución', '')).strip(),
            'department': str(row.get('Departamento', '')).strip(),
            'municipality': str(row.get('Municipio', '')).strip(),
            'daneCode': str(row.get('Código Dane', '')).strip(),
            'nit': str(row.get('NIT', '')).strip(),
            'phone': str(row.get('Teléfono', '')) if pd.notna(row.get('Teléfono')) else None,
            'email': str(row.get('Correo electrónico', '')) if pd.notna(row.get('Correo electrónico')) else None,
            'logoImg': None,
            'shieldImg': None,
            'principalSign': None,
            'website': None,
            'mission': str(row.get('Misión', '')).strip() if pd.notna(row.get('Misión')) else '',
            'vision': str(row.get('Visión', '')).strip() if pd.notna(row.get('Visión')) else '',
            'isActive': True
        }
    
    def _export_sedes(self) -> List[Dict[str, Any]]:
        """Exporta sedes/campus con estructura exacta del ejemplo"""
        if 'Sedes' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Sedes', header=1)
        
        # Usar todos los grados del sistema
        todos_los_grados = self._export_grados()
        
        sedes = []
        for idx, row in df.iterrows():
            nombre_sede = str(row.get('Nombre de la institución', '')).strip()
            
            # Intentar convertir teléfono a int, manejando strings
            telefono = row.get('Teléfono', 0)
            if pd.notna(telefono):
                try:
                    telefono = int(float(str(telefono).replace(',', '').replace('.', '')))
                except:
                    telefono = 0
            else:
                telefono = 0
            
            # Código DANE
            codigo_dane = row.get('Código Dane', 0)
            if pd.notna(codigo_dane):
                try:
                    codigo_dane = int(float(str(codigo_dane)))
                except:
                    codigo_dane = 0
            else:
                codigo_dane = 0
            
            sede = {
                'id': idx + 1,
                'Nombre sede': nombre_sede,
                'Correo': str(row.get('Correo electrónico', '')) if pd.notna(row.get('Correo electrónico')) else '',
                'Direccion': str(row.get('Dirección', '')) if pd.notna(row.get('Dirección')) else '',
                'Telefono': telefono,
                'CODIGO_DANE_SEDE': codigo_dane,
                'Grades': todos_los_grados
            }
            sedes.append(sede)
        
        return sedes
    
    def _export_cursos_academicos(self) -> List[Dict[str, Any]]:
        """Exporta cursos académicos con sus períodos"""
        if 'Cursos académicos' not in self.excel_file.sheet_names:
            return []
        
        df_cursos = self.excel_file.parse('Cursos académicos', header=1)
        df_periodos = self.excel_file.parse('Periodos', header=1) if 'Periodos' in self.excel_file.sheet_names else pd.DataFrame()
        
        cursos = []
        for _, row in df_cursos.iterrows():
            # Convertir año escolar a string consistente
            nombre_curso_raw = row.get('Nombre del año escolar', '')
            if isinstance(nombre_curso_raw, (int, float)) and not pd.isna(nombre_curso_raw):
                nombre_curso = str(int(nombre_curso_raw))
            else:
                nombre_curso = str(nombre_curso_raw).strip()
            
            # Buscar períodos de este curso
            periodos = []
            if not df_periodos.empty and 'Año escolar asociado' in df_periodos.columns:
                # Comparar convirtiendo ambos lados a string sin decimales
                for _, p_row in df_periodos.iterrows():
                    año_asociado_raw = p_row.get('Año escolar asociado', '')
                    if isinstance(año_asociado_raw, (int, float)) and not pd.isna(año_asociado_raw):
                        año_asociado = str(int(año_asociado_raw))
                    else:
                        año_asociado = str(año_asociado_raw).strip()
                    
                    if año_asociado == nombre_curso:
                        periodos.append({
                            'name': str(p_row.get('Nombre del periodo', '')).strip(),
                            'startDate': str(p_row.get('Fecha de inicio', '')) if pd.notna(p_row.get('Fecha de inicio')) else '',
                            'endDate': str(p_row.get('Fecha fin', '')) if pd.notna(p_row.get('Fecha fin')) else ''
                        })
            
            curso = {
                'name': nombre_curso,
                'startDate': str(row.get('Fecha de inicio', '')) if pd.notna(row.get('Fecha de inicio')) else '',
                'endDate': str(row.get('Fecha fin', '')) if pd.notna(row.get('Fecha fin')) else '',
                'periods': periodos
            }
            cursos.append(curso)
        
        return cursos
    
    def _export_grados(self) -> List[int]:
        """Exporta lista de niveles de grados"""
        if 'Grados' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Grados', header=1)
        grados = df['Nivel'].unique().tolist() if 'Nivel' in df.columns else []
        return sorted([int(g) for g in grados if pd.notna(g)])
    
    def _export_enriched_grades(self) -> List[Dict[str, Any]]:
        """Exporta grados enriquecidos con gradeType e isCycleCompletion"""
        if 'Grados' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Grados', header=1)
        enriched = []
        
        for _, row in df.iterrows():
            nivel = int(row['Nivel']) if pd.notna(row.get('Nivel')) else None
            if nivel is None:
                continue
            
            # Probar diferentes nombres de columna para el nombre del grado
            nombre = ''
            for col in ['Nombre del grado', 'Nombre', 'Grado']:
                if col in df.columns and pd.notna(row.get(col)):
                    nombre = str(row.get(col, '')).strip()
                    break
            
            grade_type = str(row.get('Tipo de grado', 'EDUCACION_BASICA_PRIMARIA')).strip()
            is_cycle_completion = str(row.get('¿Último grado culminante?', 'No')).lower() in ['sí', 'si', 'yes', 'true', '1']
            
            enriched.append({
                'level': nivel,
                'name': nombre,
                'gradeType': grade_type,
                'isCycleCompletion': is_cycle_completion
            })
        
        return sorted(enriched, key=lambda x: x['level'])
    
    def _get_grades_por_sede(self) -> Dict[str, List[int]]:
        """Obtiene los niveles de grados disponibles por sede desde Grupos"""
        if 'Grupos' not in self.excel_file.sheet_names:
            return {}
        
        df = self.excel_file.parse('Grupos', header=1)
        grades_por_sede = {}
        
        for _, row in df.iterrows():
            sede = str(row.get('Sedes asociadas', '')).strip()
            nombre_grado = str(row.get('Nombre del grado', '')).strip()
            nivel = self._extract_grade_level(nombre_grado)
            
            if nivel is not None:
                if sede not in grades_por_sede:
                    grades_por_sede[sede] = set()
                grades_por_sede[sede].add(nivel)
        
        # Convertir sets a listas ordenadas
        return {sede: sorted(list(grados)) for sede, grados in grades_por_sede.items()}
    
    def _export_grupos(self) -> Dict[str, Dict[int, List[str]]]:
        """Exporta grupos/aulas organizados por sede y nivel de grado"""
        if 'Grupos' not in self.excel_file.sheet_names:
            return {}
        
        df_grupos = self.excel_file.parse('Grupos', header=1)
        
        # Crear mapeo nombre_grado -> nivel desde la hoja Grados
        nombre_a_nivel = self._build_grade_name_to_level_map()
        
        grupos_por_sede = {}
        
        for _, row in df_grupos.iterrows():
            sede = str(row.get('Sedes asociadas', '')).strip()
            nombre_grado = str(row.get('Nombre del grado', '')).strip()
            nombre_grupo = str(row.get('Nombre del grupo', '')).strip()
            
            # Buscar nivel en el mapeo
            nivel = nombre_a_nivel.get(nombre_grado)
            
            if nivel is None:
                # Si no está en el mapeo, intentar extraer
                nivel = self._extract_grade_level(nombre_grado)
            
            if nivel is None:
                # Saltar grupos sin nivel identificable
                continue
            
            if sede not in grupos_por_sede:
                grupos_por_sede[sede] = {}
            
            if nivel not in grupos_por_sede[sede]:
                grupos_por_sede[sede][nivel] = []
            
            grupos_por_sede[sede][nivel].append(nombre_grupo)
        
        return grupos_por_sede
    
    def _export_asignaturas(self) -> Dict[str, List[int]]:
        """Exporta asignaturas con los grados donde se imparten"""
        if 'Asignaturas' not in self.excel_file.sheet_names:
            return {}
        
        df = self.excel_file.parse('Asignaturas', header=1)
        asignaturas = {}
        
        for _, row in df.iterrows():
            nombre = str(row.get('Nombre de la asignatura', '')).strip()
            grados_str = str(row.get('Grados asociados', ''))
            
            # Parsear grados (puede venir como "1, 2, 3" o "1,2,3")
            grados = []
            if pd.notna(grados_str) and grados_str:
                try:
                    # Extraer números de los nombres de grados
                    grados_nombres = [g.strip() for g in grados_str.split(',')]
                    grados = [self._extract_grade_level(g) for g in grados_nombres if g]
                    grados = [g for g in grados if g is not None]
                except:
                    pass
            
            asignaturas[nombre] = grados
        
        return asignaturas
    
    def _export_areas(self) -> Dict[str, List[str]]:
        """Exporta áreas académicas con sus asignaturas (relación desde hoja Asignaturas)"""
        if 'Áreas' not in self.excel_file.sheet_names:
            return {}
        
        # Primero leer todas las áreas
        df_areas = self.excel_file.parse('Áreas', header=1)
        areas = {}
        
        for _, row in df_areas.iterrows():
            nombre_area = str(row.get('Nombre del área', '')).strip()
            if nombre_area:
                areas[nombre_area] = []
        
        # Luego leer asignaturas y mapearlas a sus áreas
        if 'Asignaturas' in self.excel_file.sheet_names:
            df_asignaturas = self.excel_file.parse('Asignaturas', header=1)
            
            for _, row in df_asignaturas.iterrows():
                nombre_asignatura = str(row.get('Nombre de la asignatura', '')).strip()
                area_asociada = str(row.get('Área asociada', '')).strip()
                
                if area_asociada and area_asociada in areas and nombre_asignatura:
                    areas[area_asociada].append(nombre_asignatura)
        
        return areas
    
    def _export_administradores(self) -> List[Dict[str, Any]]:
        """Exporta administradores"""
        if 'Administradores' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Administradores', header=1)
        admins = []
        
        for _, row in df.iterrows():
            admin = {
                'name': str(row.get('Nombres', '')).strip(),
                'surname': str(row.get('Apellidos', '')).strip(),
                'email': str(row.get('Correo electrónico', '')).strip(),
                'phone': str(row.get('Teléfono', '')) if pd.notna(row.get('Teléfono')) else '',
                'documentTypeId': self._map_document_type(str(row.get('Tipo de documento', ''))),
                'documentNumber': str(row.get('Número de documento', '')),
                'password': 'Sede*2026'
            }
            admins.append(admin)
        
        return admins
    
    def _export_coordinadores(self) -> List[Dict[str, Any]]:
        """Exporta coordinadores"""
        if 'Coordinadores' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Coordinadores', header=1)
        coordinadores = []
        
        for _, row in df.iterrows():
            coord = {
                'name': str(row.get('Nombres', '')).strip(),
                'surname': str(row.get('Apellidos', '')).strip(),
                'email': str(row.get('Correo electrónico', '')).strip(),
                'phone': str(row.get('Teléfono', '')) if pd.notna(row.get('Teléfono')) else '',
                'documentTypeId': self._map_document_type(str(row.get('Tipo de documento', ''))),
                'documentNumber': str(row.get('Número de documento', '')),
                'password': 'Sede*2026',
                'campusName': str(row.get('Sede asignada', '')).strip(),
                'coordinatorType': str(row.get('Tipo de coordinador', 'ACADEMIC')).upper(),
                'isPrincipal': str(row.get('¿Coordinador principal de la sede asignada?', 'No')).lower() in ['sí', 'si', 'yes', 'true', '1']
            }
            coordinadores.append(coord)
        
        return coordinadores
    
    def export_profesores(self) -> List[Dict[str, Any]]:
        """Exporta profesores a JSON separado"""
        if 'Profesores' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Profesores', header=1)
        profesores = []
        
        for _, row in df.iterrows():
            asignaturas_str = str(row.get('Asignaturas a cargo', ''))
            asignaturas = [a.strip() for a in asignaturas_str.split(',') if a.strip()] if pd.notna(asignaturas_str) else []
            
            profesor = {
                'Nombres': str(row.get('Nombres', '')).strip(),
                'Apellidos': str(row.get('Apellidos', '')).strip(),
                'Correo': str(row.get('Correo electrónico', '')).strip(),
                'Tipo de documento': str(row.get('Tipo de documento', '')).strip(),
                'Numero de documento': str(row.get('Número de documento', '')),
                'Fecha de nacimiento': None,
                'Sexo': None,
                'Telefono': str(row.get('Teléfono', '')) if pd.notna(row.get('Teléfono')) else None,
                'Direccion': str(row.get('Dirección', '')) if pd.notna(row.get('Dirección')) else None,
                'CODIGO DANE SEDE': 0,
                'NOMBRE SEDE': str(row.get('Sede asignada', '')).strip(),
                'Asignaturas': asignaturas,
                'Grados': []
            }
            profesores.append(profesor)
        
        return profesores
    
    def export_estudiantes(self) -> List[Dict[str, Any]]:
        """Exporta estudiantes a JSON separado (desde Matrículas)"""
        if 'Matrículas' not in self.excel_file.sheet_names:
            return []
        
        df = self.excel_file.parse('Matrículas', header=1)
        estudiantes = []
        
        for _, row in df.iterrows():
            estudiante = {
                'Nombres': str(row.get('Nombres del estudiante', '')).strip(),
                'Apellidos': str(row.get('Apellidos del estudiante', '')).strip(),
                'Correo': str(row.get('Correo del estudiante', '')) if pd.notna(row.get('Correo del estudiante')) else '',
                'Tipo de documento': str(row.get('Tipo de documento del estudiante', '')).strip(),
                'Numero de documento': str(row.get('Número de documento del estudiante', '')),
                'Grado': self._extract_grade_level(str(row.get('Nombre del grado', ''))) or 0,
                'Sexo': str(row.get('Sexo del estudiante', '')).strip(),
                'Fecha de nacimiento': str(row.get('Fecha de nacimiento del estudiante', '')),
                'Direccion': None,
                'Tipo de sangre': None,
                'CODIGO DANE SEDE A LA QUE PERTENECE': 0,
                'NOMBRE SEDE': str(row.get('Sede asociada', '')).strip(),
                'AULA DE ESTUDIO': str(row.get('Nombre del grupo', '')).strip(),
                'CEDULA ACUDIENTE': str(row.get('Número de documento del acudiente', '')) if pd.notna(row.get('Número de documento del acudiente')) else '',
                'Telefono': None,
                'CURSO': str(row.get('Nombre del año escolar', '')).strip()
            }
            estudiantes.append(estudiante)
        
        return estudiantes
    
    def export_calificaciones(self) -> Dict[str, Dict[str, Any]]:
        """Exporta calificaciones anuales agrupadas por estudiante (filtrando asignaturas inválidas)"""
        if 'Calificaciones anuales' not in self.excel_file.sheet_names:
            return {}
        
        df = self.excel_file.parse('Calificaciones anuales', header=1)
        
        # Obtener asignaturas válidas del contexto
        asignaturas_validas = set()
        if 'Asignaturas' in self.excel_file.sheet_names:
            df_asignaturas = self.excel_file.parse('Asignaturas', header=1)
            if 'Nombre de la asignatura' in df_asignaturas.columns:
                asignaturas_validas = set(df_asignaturas['Nombre de la asignatura'].dropna().unique())
        
        # Agrupar por estudiante (número de documento + año escolar + sede)
        estudiantes_agrupados = {}
        
        for _, row in df.iterrows():
            asignatura = str(row.get('Nombre de la asignatura', '')).strip()
            
            # Filtrar registros con asignaturas inválidas
            if asignaturas_validas and asignatura not in asignaturas_validas:
                continue
            
            # Convertir año escolar a string sin decimales si es número
            año_escolar = row.get('Año escolar', '')
            if isinstance(año_escolar, (int, float)) and not pd.isna(año_escolar):
                año_escolar = str(int(año_escolar))
            else:
                año_escolar = str(año_escolar).strip()
            
            # Extraer campos
            num_documento = str(row.get('Número de documento del estudiante', '')).strip()
            nombre_estudiante = str(row.get('Nombre del estudiante', '')).strip()
            sede_asignada = str(row.get('Sede asignada', '')).strip()
            tipo_nota = str(row.get('Tipo de nota', '')).strip()
            aprobo = str(row.get('Aprobó', '')) if pd.notna(row.get('Aprobó')) else None
            promedio_anual = row.get('Promedio anual')
            
            # Crear clave compuesta si el estudiante tiene múltiples años o sedes
            # Por ahora usamos solo documento + año escolar + sede para agrupar
            clave_base = f"{num_documento}_{año_escolar}_{sede_asignada}"
            
            # Si el estudiante no existe, crearlo
            if clave_base not in estudiantes_agrupados:
                estudiantes_agrupados[clave_base] = {
                    'numero_documento': num_documento,
                    'año_escolar': año_escolar,
                    'sede_asignada': sede_asignada,
                    'Nombre del estudiante': nombre_estudiante,
                    'Año escolar': año_escolar,
                    'Sede asignada': sede_asignada,
                    'Tipo de nota': tipo_nota,
                    'Aprobó': aprobo,
                    'calificaciones': [],
                    'asignaturas_vistas': {}  # Para evitar duplicados
                }
            
            # Agregar calificación solo si no existe ya esta asignatura
            # Si existe, actualizar con el último valor (sobrescribir)
            if asignatura not in estudiantes_agrupados[clave_base]['asignaturas_vistas']:
                estudiantes_agrupados[clave_base]['calificaciones'].append({
                    'Nombre de la asignatura': asignatura,
                    'Promedio anual': promedio_anual
                })
                estudiantes_agrupados[clave_base]['asignaturas_vistas'][asignatura] = len(estudiantes_agrupados[clave_base]['calificaciones']) - 1
            else:
                # Ya existe, actualizar el valor en su posición
                idx = estudiantes_agrupados[clave_base]['asignaturas_vistas'][asignatura]
                estudiantes_agrupados[clave_base]['calificaciones'][idx]['Promedio anual'] = promedio_anual
        
        # Transformar a estructura final: usar solo documento si hay un solo año/sede por estudiante
        calificaciones_finales = {}
        
        # Agrupar por número de documento para verificar cuántas combinaciones año/sede tiene cada estudiante
        docs_agrupados = {}
        for clave, datos in estudiantes_agrupados.items():
            doc = datos['numero_documento']
            if doc not in docs_agrupados:
                docs_agrupados[doc] = []
            docs_agrupados[doc].append((clave, datos))
        
        # Decidir clave final: solo documento o documento_año_sede
        for doc, entradas in docs_agrupados.items():
            if len(entradas) == 1:
                # Un solo año/sede: usar solo el número de documento
                clave, datos = entradas[0]
                # Eliminar campos auxiliares
                datos_finales = {k: v for k, v in datos.items() if k not in ['numero_documento', 'año_escolar', 'sede_asignada', 'asignaturas_vistas']}
                calificaciones_finales[doc] = datos_finales
            else:
                # Múltiples años/sedes: usar clave compuesta
                for clave, datos in entradas:
                    clave_final = f"{doc}_{datos['año_escolar']}_{datos['sede_asignada']}"
                    # Eliminar campos auxiliares
                    datos_finales = {k: v for k, v in datos.items() if k not in ['numero_documento', 'año_escolar', 'sede_asignada', 'asignaturas_vistas']}
                    calificaciones_finales[clave_final] = datos_finales
        
        return calificaciones_finales
    
    # Métodos auxiliares
    
    def _build_grade_name_to_level_map(self) -> Dict[str, int]:
        """Construye un mapeo de nombre de grado a nivel desde la hoja Grados"""
        if 'Grados' not in self.excel_file.sheet_names:
            return {}
        
        df = self.excel_file.parse('Grados', header=1)
        mapeo = {}
        
        for _, row in df.iterrows():
            nivel = row.get('Nivel')
            if pd.notna(nivel):
                nivel = int(nivel)
                
                # Intentar diferentes columnas para el nombre
                for col in ['Nombre del grado', 'Nombre', 'Grado']:
                    if col in df.columns and pd.notna(row.get(col)):
                        nombre = str(row.get(col, '')).strip()
                        if nombre:
                            mapeo[nombre] = nivel
                        break
        
        return mapeo
    
    def _extract_grade_level(self, nombre_grado: str) -> int:
        """Extrae el nivel numérico de un nombre de grado"""
        mapeo_grados = {
            'Pre-jardín': -1,
            'Jardín': 0,
            'Transición': 0,
            'Primero': 1,
            'Segundo': 2,
            'Tercero': 3,
            'Cuarto': 4,
            'Quinto': 5,
            'Sexto': 6,
            'Séptimo': 7,
            'Octavo': 8,
            'Noveno': 9,
            'Décimo': 10,
            'Undécimo': 11,
            'Once': 11
        }
        
        nombre_clean = nombre_grado.strip()
        for nombre, nivel in mapeo_grados.items():
            if nombre.lower() in nombre_clean.lower():
                return nivel
        
        # Intentar extraer número directamente
        import re
        match = re.search(r'\d+', nombre_clean)
        if match:
            return int(match.group())
        
        return None
    
    def _get_default_school(self) -> Dict[str, Any]:
        """Retorna configuración de escuela por defecto"""
        return {
            'name': 'Institución Educativa',
            'department': '',
            'municipality': '',
            'daneCode': '',
            'nit': '',
            'phone': None,
            'email': None,
            'logoImg': None,
            'shieldImg': None,
            'principalSign': None,
            'website': None,
            'mission': '',
            'vision': '',
            'isActive': True
        }
    
    def _get_default_session_types(self) -> List[Dict[str, Any]]:
        """Retorna tipos de sesión por defecto"""
        return [
            {'name': 'Mañana', 'startHour': 6, 'endHour': 12},
            {'name': 'Tarde', 'startHour': 12, 'endHour': 18},
            {'name': 'Única', 'startHour': 6, 'endHour': 18}
        ]
    
    def _get_default_leveling_rule(self) -> Dict[str, Any]:
        """Retorna regla de nivelación por defecto"""
        return {
            'maxFailedSubjects': 2,
            'maxUnjustifiedAbsences': 5,
            'sessionTypeIds': [1],
            'isActive': True
        }
    
    def _map_document_type(self, tipo: str) -> int:
        """Mapea tipo de documento a ID (según esquema del backend)"""
        tipo_lower = tipo.lower().strip()
        
        # Mapeo basado en el sistema del backend
        if 'cédula de ciudadanía' in tipo_lower or 'cedula de ciudadania' in tipo_lower or tipo_lower == 'cc':
            return 5
        elif 'tarjeta de identidad' in tipo_lower or tipo_lower == 'ti':
            return 3
        elif 'registro civil' in tipo_lower or tipo_lower == 'rc':
            return 4
        elif 'cédula de extranjería' in tipo_lower or 'cedula de extranjeria' in tipo_lower or tipo_lower == 'ce':
            return 2
        elif 'pasaporte' in tipo_lower:
            return 1
        else:
            return 5  # Por defecto CC
    
    def save_to_files(self, output_dir: str = 'output'):
        """
        Guarda los JSONs en archivos separados
        
        Args:
            output_dir: Directorio donde guardar los archivos
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        data = self.export_all()
        
        # Guardar config.json
        with open(os.path.join(output_dir, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(data['config'], f, ensure_ascii=False, indent=2)
        
        # Guardar profesores.json
        with open(os.path.join(output_dir, 'profesores.json'), 'w', encoding='utf-8') as f:
            json.dump(data['profesores'], f, ensure_ascii=False, indent=2)
        
        # Guardar estudiantes.json
        with open(os.path.join(output_dir, 'estudiantes.json'), 'w', encoding='utf-8') as f:
            json.dump(data['estudiantes'], f, ensure_ascii=False, indent=2)
        
        # Guardar calificaciones_anuales.json
        with open(os.path.join(output_dir, 'calificaciones_anuales.json'), 'w', encoding='utf-8') as f:
            json.dump(data['calificaciones_anuales'], f, ensure_ascii=False, indent=2)
        
        return {
            'config': os.path.join(output_dir, 'config.json'),
            'profesores': os.path.join(output_dir, 'profesores.json'),
            'estudiantes': os.path.join(output_dir, 'estudiantes.json'),
            'calificaciones_anuales': os.path.join(output_dir, 'calificaciones_anuales.json')
        }


# Función auxiliar para uso directo
def export_excel_to_json(excel_path: str, output_dir: str = 'output'):
    """
    Exporta un archivo Excel a formato JSON
    
    Args:
        excel_path: Ruta al archivo Excel
        output_dir: Directorio de salida
        
    Returns:
        Dict con rutas de los archivos generados
    """
    excel_file = pd.ExcelFile(excel_path)
    exporter = ExcelToJSONExporter(excel_file)
    return exporter.save_to_files(output_dir)
