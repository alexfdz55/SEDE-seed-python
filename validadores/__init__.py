# Importar todos los validadores
from .sede_principal import validar_sede_principal
from .sedes import validar_sedes
from .administradores import validar_administradores
from .coordinadores import validar_coordinadores
from .cursos_academicos import validar_cursos_academicos
from .periodos import validar_periodos
from .grados import validar_grados
from .grupos import validar_grupos
from .areas import validar_areas
from .asignaturas import validar_asignaturas
from .profesores import validar_profesores
from .clases import validar_clases
from .matriculas import validar_matriculas
from .calificaciones_anuales import validar_calificaciones_anuales

# Mapa de validadores por hoja
VALIDADORES = {
    "Sede principal": validar_sede_principal,
    "Sedes": validar_sedes,
    "Administradores": validar_administradores,
    "Coordinadores": validar_coordinadores,
    "Cursos académicos": validar_cursos_academicos,
    "Periodos": validar_periodos,
    "Grados": validar_grados,
    "Grupos": validar_grupos,
    "Áreas": validar_areas,
    "Asignaturas": validar_asignaturas,
    "Profesores": validar_profesores,
    "Clases": validar_clases,
    "Matrículas": validar_matriculas,
    "Calificaciones anuales": validar_calificaciones_anuales
}
