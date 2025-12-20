import pandas as pd

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

# Ruta del archivo Excel
archivo_excel = "seed_Pablo_Neruda.xlsx"

# Leer todas las hojas del Excel
excel_file = pd.ExcelFile(archivo_excel)

# Mostrar los nombres de todas las hojas
print("Hojas en el archivo Excel:")
print("-" * 40)
for i, nombre_hoja in enumerate(excel_file.sheet_names, 1):
    print(f"{i}. {nombre_hoja}")

# Validar que el Excel tenga todas las hojas requeridas
print("\n" + "=" * 40)
print("Validación de hojas:")
print("=" * 40)

hojas_faltantes = [hoja for hoja in HOJAS_REQUERIDAS if hoja not in excel_file.sheet_names]
hojas_extra = [hoja for hoja in excel_file.sheet_names if hoja not in HOJAS_REQUERIDAS]

if not hojas_faltantes and not hojas_extra:
    print("✓ El archivo tiene todas las hojas requeridas")
else:
    if hojas_faltantes:
        print(f"✗ Faltan {len(hojas_faltantes)} hoja(s):")
        for hoja in hojas_faltantes:
            print(f"  - {hoja}")
    
    if hojas_extra:
        print(f"⚠ Hay {len(hojas_extra)} hoja(s) adicional(es):")
        for hoja in hojas_extra:
            print(f"  - {hoja}")
