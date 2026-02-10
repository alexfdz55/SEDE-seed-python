import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import warnings
import json
import zipfile
from config import HOJAS_REQUERIDAS, COLUMNAS_REQUERIDAS
from validador_core import construir_contexto, validar_hoja
from exportador_json import ExcelToJSONExporter

# Configuración de página
st.set_page_config(
    page_title="Validador Excel - Seed Pablo Neruda",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.3rem;
        padding: 1rem;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.3rem;
        padding: 1rem;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

def validar_excel(archivo_excel):
    """
    Valida el archivo Excel y retorna resultados
    """
    resultados = {
        'hojas_validas': [],
        'hojas_con_errores': [],
        'total_errores': 0,
        'total_advertencias': 0,
        'detalles': {}
    }
    
    try:
        excel_file = pd.ExcelFile(archivo_excel)
        
        # Construir contexto
        contexto = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_hojas = len(HOJAS_REQUERIDAS) - 1  # Sin Instrucciones
        hoja_actual = 0
        
        # Primera pasada: construir contexto
        status_text.text("🔄 Construyendo contexto de referencia...")
        contexto = construir_contexto(excel_file, archivo_excel)
        
        # Segunda pasada: validar hojas
        for hoja in HOJAS_REQUERIDAS:
            if hoja == "Instrucciones":
                continue
            
            hoja_actual += 1
            progreso = hoja_actual / total_hojas
            progress_bar.progress(progreso)
            status_text.text(f"📋 Validando: {hoja} ({hoja_actual}/{total_hojas})")
            
            resultado_hoja = {
                'nombre': hoja,
                'existe': False,
                'estructura_valida': False,
                'contenido_valido': False,
                'errores': [],
                'advertencias': [],
                'num_filas': 0
            }
            
            if hoja not in excel_file.sheet_names:
                resultado_hoja['errores'].append(f"La hoja '{hoja}' no existe")
                resultados['detalles'][hoja] = resultado_hoja
                resultados['hojas_con_errores'].append(hoja)
                resultados['total_errores'] += 1
                continue
            
            resultado_hoja['existe'] = True
            df = pd.read_excel(excel_file, sheet_name=hoja, header=1)
            resultado_hoja['num_filas'] = len(df)
            
            # Validar estructura (columnas)
            if hoja in COLUMNAS_REQUERIDAS:
                columnas_requeridas = COLUMNAS_REQUERIDAS[hoja]
                columnas_presentes = df.columns.tolist()
                
                if columnas_requeridas == columnas_presentes[:len(columnas_requeridas)]:
                    resultado_hoja['estructura_valida'] = True
                else:
                    resultado_hoja['errores'].append("Estructura de columnas incorrecta")
            
            # Validar contenido
            validacion = validar_hoja(hoja, df, contexto)
            resultado_hoja['contenido_valido'] = validacion['valido']
            resultado_hoja['errores'].extend(validacion['errores'])
            resultado_hoja['advertencias'].extend(validacion['advertencias'])
            
            # Agregar a resultados
            resultados['detalles'][hoja] = resultado_hoja
            resultados['total_errores'] += len(resultado_hoja['errores'])
            resultados['total_advertencias'] += len(resultado_hoja['advertencias'])
            
            if len(resultado_hoja['errores']) > 0:
                resultados['hojas_con_errores'].append(hoja)
            elif resultado_hoja['estructura_valida'] and resultado_hoja['contenido_valido']:
                resultados['hojas_validas'].append(hoja)
        
        progress_bar.progress(1.0)
        status_text.text("✅ Validación completada")
        
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        return None
    
    return resultados

def generar_reporte_csv(resultados):
    """Genera un CSV con el resumen de errores"""
    datos = []
    for hoja, detalle in resultados['detalles'].items():
        for error in detalle['errores']:
            datos.append({
                'Hoja': hoja,
                'Tipo': 'Error',
                'Mensaje': error,
                'Filas': detalle['num_filas']
            })
        for advertencia in detalle['advertencias']:
            datos.append({
                'Hoja': hoja,
                'Tipo': 'Advertencia',
                'Mensaje': advertencia,
                'Filas': detalle['num_filas']
            })
    
    df = pd.DataFrame(datos)
    return df.to_csv(index=False).encode('utf-8-sig')

# Header
st.markdown('<div class="main-header">📊 Validador de Excel - Seed Pablo Neruda</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📁 Cargar Archivo")
    st.markdown("---")
    
    archivo_cargado = st.file_uploader(
        "Selecciona archivo Excel",
        type=['xlsx', 'xls'],
        help="Arrastra y suelta o haz clic para seleccionar"
    )
    
    st.markdown("---")
    st.subheader("ℹ️ Información")
    st.info("""
    **Sistema de validación completo**
    
    ✓ 15 hojas validadas  
    ✓ Integridad referencial  
    ✓ Detección de duplicados  
    ✓ Validación de formatos  
    """)
    
    st.markdown("---")
    st.caption("🎓 INSTITUCIÓN EDUCATIVA PABLO NERUDA")

# Contenido principal
if archivo_cargado is None:
    # Estado inicial - sin archivo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/clouds/400/ms-excel.png", width=200)
        st.markdown("""
        <div style='text-align: center;'>
            <h3>👈 Carga un archivo Excel para comenzar</h3>
            <p style='color: #666;'>El sistema validará automáticamente todas las hojas y mostrará un reporte detallado</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 Hojas que se validarán"):
        for i, hoja in enumerate(HOJAS_REQUERIDAS[1:], 1):
            st.write(f"{i}. {hoja}")

else:
    # Archivo cargado - ejecutar validación
    st.success(f"✅ Archivo cargado: **{archivo_cargado.name}**")
    
    # Ejecutar validación
    with st.spinner("Validando archivo..."):
        resultados = validar_excel(archivo_cargado)
    
    if resultados:
        # Métricas principales
        st.markdown("### 📊 Resumen de Validación")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Errores",
                resultados['total_errores'],
                delta=None,
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Advertencias",
                resultados['total_advertencias'],
                delta=None,
                delta_color="normal"
            )
        
        with col3:
            hojas_validas = len(resultados['hojas_validas'])
            total_hojas = len(HOJAS_REQUERIDAS) - 1
            st.metric(
                "Hojas Válidas",
                f"{hojas_validas}/{total_hojas}",
                delta=None
            )
        
        with col4:
            if resultados['total_errores'] == 0:
                st.markdown('<div class="success-box"><b>✅ VÁLIDO</b></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box"><b>❌ CON ERRORES</b></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Gráficos
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Gráfico de barras: Errores por hoja
            errores_por_hoja = {hoja: len(detalle['errores']) 
                               for hoja, detalle in resultados['detalles'].items() 
                               if len(detalle['errores']) > 0}
            
            if errores_por_hoja:
                fig_errores = go.Figure(data=[
                    go.Bar(
                        x=list(errores_por_hoja.keys()),
                        y=list(errores_por_hoja.values()),
                        marker_color='#e74c3c'
                    )
                ])
                fig_errores.update_layout(
                    title="Errores por Hoja",
                    xaxis_title="Hoja",
                    yaxis_title="Cantidad de Errores",
                    height=400
                )
                st.plotly_chart(fig_errores, width='stretch')
            else:
                st.success("🎉 No hay errores en ninguna hoja")
        
        with col_right:
            # Gráfico circular: Estado de hojas
            estado_hojas = {
                'Válidas': len(resultados['hojas_validas']),
                'Con Errores': len(resultados['hojas_con_errores']),
            }
            
            fig_estado = go.Figure(data=[
                go.Pie(
                    labels=list(estado_hojas.keys()),
                    values=list(estado_hojas.values()),
                    marker_colors=['#2ecc71', '#e74c3c']
                )
            ])
            fig_estado.update_layout(
                title="Estado de las Hojas",
                height=400
            )
            st.plotly_chart(fig_estado, width='stretch')
        
        st.markdown("---")
        
        # Detalles por hoja (tabs)
        st.markdown("### 📋 Detalles por Hoja")
        
        tabs = st.tabs([hoja for hoja in resultados['detalles'].keys()])
        
        for tab, (hoja, detalle) in zip(tabs, resultados['detalles'].items()):
            with tab:
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric("Filas", detalle['num_filas'])
                with col_info2:
                    estado = "✅ Válida" if detalle['contenido_valido'] and len(detalle['errores']) == 0 else "❌ Con Errores"
                    st.markdown(f"**Estado:** {estado}")
                
                if len(detalle['errores']) > 0:
                    st.error("**Errores encontrados:**")
                    for i, error in enumerate(detalle['errores'], 1):
                        st.write(f"{i}. {error}")
                
                if len(detalle['advertencias']) > 0:
                    st.warning("**Advertencias:**")
                    for i, adv in enumerate(detalle['advertencias'], 1):
                        st.write(f"{i}. {adv}")
                
                if len(detalle['errores']) == 0 and len(detalle['advertencias']) == 0:
                    st.success("✅ No hay errores ni advertencias en esta hoja")
        
        st.markdown("---")
        
        # Descarga de reportes
        st.markdown("### 💾 Descargar Reportes")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            csv_reporte = generar_reporte_csv(resultados)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_reporte,
                file_name="reporte_validacion.csv",
                mime="text/csv"
            )
        
        with col_btn2:
            # Resumen en texto
            resumen_txt = f"""REPORTE DE VALIDACIÓN - {archivo_cargado.name}
{'='*80}

RESUMEN:
- Total de errores: {resultados['total_errores']}
- Total de advertencias: {resultados['total_advertencias']}
- Hojas válidas: {len(resultados['hojas_validas'])}/{len(HOJAS_REQUERIDAS)-1}

{'='*80}

DETALLES POR HOJA:

"""
            for hoja, detalle in resultados['detalles'].items():
                resumen_txt += f"\n{hoja}:\n"
                resumen_txt += f"  - Filas: {detalle['num_filas']}\n"
                if detalle['errores']:
                    resumen_txt += f"  - Errores:\n"
                    for error in detalle['errores']:
                        resumen_txt += f"    * {error}\n"
                if detalle['advertencias']:
                    resumen_txt += f"  - Advertencias:\n"
                    for adv in detalle['advertencias']:
                        resumen_txt += f"    * {adv}\n"
            
            st.download_button(
                label="📥 Descargar TXT",
                data=resumen_txt.encode('utf-8'),
                file_name="reporte_validacion.txt",
                mime="text/plain"
            )
        
        with col_btn3:
            # Opción para forzar exportación aun con errores
            force_export = st.checkbox("Forzar exportación (ignorar errores)", value=False)

            # Exportar a JSON
            if resultados['total_errores'] == 0 or force_export:
                try:
                    if resultados['total_errores'] > 0 and force_export:
                        st.info("🔔 Exportando aún con errores: revisa las advertencias y el resultado antes de usarlo en producción.")
                    # Crear exportador
                    excel_file = pd.ExcelFile(archivo_cargado)
                    exporter = ExcelToJSONExporter(excel_file)
                    data = exporter.export_all()
                    
                    # Crear ZIP con todos los JSONs
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        # Agregar config.json
                        zip_file.writestr('config.json', 
                                        json.dumps(data['config'], ensure_ascii=False, indent=2))
                        # Agregar profesores.json
                        zip_file.writestr('profesores.json', 
                                        json.dumps(data['profesores'], ensure_ascii=False, indent=2))
                        # Agregar estudiantes.json
                        zip_file.writestr('estudiantes.json', 
                                        json.dumps(data['estudiantes'], ensure_ascii=False, indent=2))
                        # Agregar calificaciones_anuales.json
                        zip_file.writestr('calificaciones_anuales.json', 
                                        json.dumps(data['calificaciones_anuales'], ensure_ascii=False, indent=2))
                    
                    zip_buffer.seek(0)
                    
                    st.download_button(
                        label="📦 Exportar a JSON",
                        data=zip_buffer.getvalue(),
                        file_name="seed_data.zip",
                        mime="application/zip",
                        help="Descarga 4 archivos JSON: config, profesores, estudiantes y calificaciones"
                    )
                except Exception as e:
                    st.error(f"Error al exportar JSON: {str(e)}")
            else:
                st.warning("⚠️ Corrige los errores antes de exportar")

