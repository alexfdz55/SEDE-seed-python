import pandas as pd
from config import HOJAS_REQUERIDAS, COLUMNAS_REQUERIDAS
from validador_core import construir_contexto, validar_hoja
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

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

# Validación de columnas y contenido
print("\n" + "=" * 40)
print("Validación de columnas y contenido:")
print("=" * 40)

total_errores = 0
total_advertencias = 0

# Construir contexto (reutilizando función compartida)
contexto = construir_contexto(excel_file, archivo_excel)

# Validar cada hoja
for nombre_hoja in excel_file.sheet_names:
    # Saltar la hoja de Instrucciones
    if nombre_hoja == "Instrucciones":
        continue
    
    # Leer la hoja
    df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja, header=1)
    
    columnas_actuales = list(df.columns)
    columnas_esperadas = COLUMNAS_REQUERIDAS[nombre_hoja]
    
    # Validar columnas
    columnas_faltantes = [col for col in columnas_esperadas if col not in columnas_actuales]
    columnas_extra = [col for col in columnas_actuales if col not in columnas_esperadas]
    
    print(f"\n{nombre_hoja}:")
    
    # Validar estructura de columnas
    if not columnas_faltantes and not columnas_extra:
        print(f"  ✓ Estructura correcta ({len(columnas_actuales)} columnas)")
    else:
        if columnas_faltantes:
            print(f"  ✗ Faltan {len(columnas_faltantes)} columna(s):")
            for col in columnas_faltantes:
                print(f"    - {col}")
            total_errores += len(columnas_faltantes)
        
        if columnas_extra:
            print(f"  ⚠ Hay {len(columnas_extra)} columna(s) adicional(es):")
            for col in columnas_extra:
                print(f"    - {col}")
            total_advertencias += len(columnas_extra)
    
    # Validar contenido (reutilizando función compartida)
    resultado = validar_hoja(nombre_hoja, df, contexto)
    
    if resultado['valido']:
        print(f"  ✓ Contenido válido ({len(df)} fila(s))")
    else:
        print(f"  ✗ Problemas en el contenido:")
        
    if resultado['errores']:
        for error in resultado['errores']:
            print(f"    ✗ {error}")
            total_errores += 1
    
    if resultado['advertencias']:
        for advertencia in resultado['advertencias']:
            print(f"    ⚠ {advertencia}")
            total_advertencias += 1

# Resumen final
print("\n" + "=" * 40)
print("RESUMEN DE VALIDACIÓN:")
print("=" * 40)
print(f"Total de errores: {total_errores}")
print(f"Total de advertencias: {total_advertencias}")

if total_errores == 0:
    print("\n✓ El archivo Excel es VÁLIDO")
else:
    print(f"\n✗ El archivo Excel tiene {total_errores} error(es) que deben corregirse")
