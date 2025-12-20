# Configuración de validación para archivos Excel de semilla

# Hojas requeridas en el Excel
HOJAS_REQUERIDAS = [
    "Instrucciones",
    "Sede principal",
    "Sedes",
    "Administradores",
    "Coordinadores",
    "Cursos académicos",
    "Periodos",
    "Grados",
    "Grupos",
    "Áreas",
    "Asignaturas",
    "Profesores",
    "Clases",
    "Matrículas",
    "Calificaciones anuales"
]

# Columnas requeridas por cada hoja (excepto Instrucciones)
COLUMNAS_REQUERIDAS = {
    "Sede principal": [
        "Nombre de la institución",
        "INSTITUCIÓN EDUCATIVA PABLO NERUDA"
    ],
    "Sedes": [
        "Nombre de la institución",
        "Dirección",
        "Teléfono",
        "Correo electrónico",
        "Código Dane"
    ],
    "Administradores": [
        "Nombres",
        "Apellidos",
        "Correo electrónico",
        "Tipo de documento",
        "Número de documento",
        "Teléfono"
    ],
    "Coordinadores": [
        "Nombres",
        "Apellidos",
        "Correo electrónico",
        "Tipo de documento",
        "Número de documento",
        "Teléfono",
        "Sede asignada",
        "Tipo de coordinador",
        "¿Coordinador principal de la sede asignada?"
    ],
    "Cursos académicos": [
        "Nombre del año escolar",
        "Fecha de inicio",
        "Fecha fin"
    ],
    "Periodos": [
        "Nombre del periodo",
        "Fecha de inicio",
        "Fecha fin",
        "Año escolar asociado"
    ],
    "Grados": [
        "Nivel",
        "Nombre del grado",
        "Tipo de grado",
        "¿Último grado culminante?"
    ],
    "Grupos": [
        "Nombre del grupo",
        "Nombre del grado",
        "Sedes asociadas",
        "Capacidad"
    ],
    "Áreas": [
        "Nombre del área"
    ],
    "Asignaturas": [
        "Nombre de la asignatura",
        "Área asociada",
        "Grados asociados"
    ],
    "Profesores": [
        "Nombres",
        "Apellidos",
        "Tipo de documento",
        "Número de documento",
        "Teléfono",
        "Dirección",
        "Correo electrónico",
        "Sede asignada",
        "Asignaturas a cargo"
    ],
    "Clases": [
        "Nombre de la asignatura",
        "Nombre del grado",
        "Nombre del grupo",
        "Sede asociada",
        "Año escolar asociado",
        "Periodos asociados",
        "Jornada",
        "Nombre del profesor a cargo",
        "Número de documento del profesor"
    ],
    "Matrículas": [
        "Número de documento",
        "Tipo de documento",
        "Nombres",
        "Apellidos",
        "Fecha de nacimiento",
        "Sede asignada",
        "Año escolar",
        "Grado",
        "Grupo",
        "Correo electrónico",
        "Teléfono",
        "Número de matrícula",
        "Fecha de matrícula",
        "Jornada",
        "Sexo",
        "Municipio de residencia",
        "Dirección",
        "Lugar de nacimiento",
        "Lugar de expedición del documento",
        "Barrio/Vereda",
        "EPS",
        "Grupo Étnico",
        "Tipo de sangre",
        "¿Vive con sus padres?",
        "¿Con quién vive?",
        "¿Hermanos en la institución?¿Cuantos?",
        "Grados de los Hermanos",
        "Tipo de discapacidad",
        "¿Es repitente?",
        "Nivel SISBEN",
        "Fecha de Retiro",
        "Causa de Retiro",
        "Nombres.1",
        "Apellidos.1",
        "Tipo de documento.1",
        "Número de documento.1",
        "Parentesco",
        "Correo electrónico.1",
        "Teléfono.1",
        "Dirección.1",
        "Municipio de residencia.1",
        "Nombres.2",
        "Apellidos.2",
        "Tipo de documento.2",
        "Número de documento.2",
        "Parentesco.1",
        "Correo electrónico.2",
        "Teléfono.2",
        "Dirección.2",
        "Municipio de residencia.2",
        "Nombres.3",
        "Apellidos.3",
        "Tipo de documento.3",
        "Número de documento.3",
        "Parentesco.2",
        "Correo electrónico.3",
        "Teléfono.3",
        "Dirección.3",
        "Municipio de residencia.3"
    ],
    "Calificaciones anuales": [
        "Número de documento del estudiante",
        "Nombre del estudiante",
        "Nombre de la asignatura",
        "Año escolar",
        "Sede asignada",
        "Tipo de nota",
        "Promedio anual",
        "Aprobó"
    ]
}
