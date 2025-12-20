import pandas as pd
import warnings
from config import HOJAS_REQUERIDAS, COLUMNAS_REQUERIDAS

# Suprimir warnings de openpyxl sobre validación de datos
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

# Leer las columnas de todas las hojas (excepto la primera "Instrucciones")
print("\n" + "=" * 40)
print("Validación de columnas:")
print("=" * 40)

for nombre_hoja in excel_file.sheet_names:
    # Saltar la hoja de Instrucciones
    if nombre_hoja == "Instrucciones":
        continue
    
    # Leer la hoja - intentar con header en la segunda fila (índice 1)
    df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja, header=1)
    
    columnas_actuales = list(df.columns)
    columnas_esperadas = COLUMNAS_REQUERIDAS[nombre_hoja]
    
    # Validar columnas
    columnas_faltantes = [col for col in columnas_esperadas if col not in columnas_actuales]
    columnas_extra = [col for col in columnas_actuales if col not in columnas_esperadas]
    
    print(f"\n{nombre_hoja}:")
    if not columnas_faltantes and not columnas_extra:
        print(f"  ✓ Todas las columnas son correctas ({len(columnas_actuales)})")
    else:
        if columnas_faltantes:
            print(f"  ✗ Faltan {len(columnas_faltantes)} columna(s):")
            for col in columnas_faltantes:
                print(f"    - {col}")
        
        if columnas_extra:
            print(f"  ⚠ Hay {len(columnas_extra)} columna(s) adicional(es):")
            for col in columnas_extra:
                print(f"    - {col}")
