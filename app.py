# app.py
"""
Aplicación Web Interactiva con Streamlit (Ampliación A10).
"""

import streamlit as st
import matplotlib.pyplot as plt
from motor_reglas import encadenar_hacia_adelante
from logica_difusa import inferir_desvio, generar_grafico_difuso

st.set_page_config(page_title="Gestión de Incidencias Logísticas", page_icon="📦", layout="wide")

st.title("📦 Sistema Experto y Difuso de Gestión Logística")
st.markdown("Prototipo explicable para control de incidencias y gestión gradual de ocupación.")

tab1, tab2 = st.tabs(["1. Sistema Experto (Motor de Reglas)", "2. Lógica Difusa (Ocupación de Zonas)"])

with tab1:
    st.header("Evaluación de Incidencias en Paquetes")
    st.write("Seleccione las características observables del paquete:")
    
    col1, col2 = st.columns(2)
    with col1:
        c_no_legible = st.checkbox("Código de barras no legible (`codigo_no_legible`)")
        d_no_identificado = st.checkbox("Destino no identificado (`destino_no_identificado`)")
        d_identificado = st.checkbox("Destino identificado (`destino_identificado`)")
        e_danado = st.checkbox("Embalaje dañado (`embalaje_danado`)")
    with col2:
        c_fragil = st.checkbox("Contenido frágil (`contenido_fragil`)")
        p_fuera_rango = st.checkbox("Peso fuera de rango (`peso_fuera_rango`)")
        doc_incompleta = st.checkbox("Documentación incompleta (`documentacion_incompleta`)")
        sin_incidencias = st.checkbox("Sin incidencias observadas (`sin_incidencias`)")
        
    hechos_input = set()
    if c_no_legible: hechos_input.add("codigo_no_legible")
    if d_no_identificado: hechos_input.add("destino_no_identificado")
    if d_identificado: hechos_input.add("destino_identificado")
    if e_danado: hechos_input.add("embalaje_danado")
    if c_fragil: hechos_input.add("contenido_fragil")
    if p_fuera_rango: hechos_input.add("peso_fuera_rango")
    if doc_incompleta: hechos_input.add("documentacion_incompleta")
    if sin_incidencias: hechos_input.add("sin_incidencias")
    
    if st.button("Ejecutar Inferencia", type="primary"):
        hechos_finales, traza = encadenar_hacia_adelante(hechos_input)
        
        st.subheader("Resultado del Razonamiento")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("**Hechos Iniciales:**")
            st.json(list(hechos_input))
            
        with col_res2:
            st.markdown("**Nuevas Conclusiones Generadas:**")
            conclusiones = list(hechos_finales - hechos_input)
            if conclusiones:
                st.success(", ".join(conclusiones))
            else:
                st.warning("No se generaron nuevas conclusiones.")
                
        st.subheader("Traza de Inferencia Explicable")
        if traza:
            for i, paso in enumerate(traza, 1):
                st.info(f"**Paso {i} [{paso['regla']}]:** Si ({' + '.join(paso['condiciones'])}) $\rightarrow$ **{paso['conclusion']}**")
        else:
            st.write("No se activó ninguna regla.")

with tab2:
    st.header("Gestión Gradual de Ocupación por Lógica Difusa")
    
    ocupacion_val = st.slider(
        "Seleccione el nivel de ocupación de la zona (%):",
        min_value=0.0, max_value=100.0, value=80.0, step=0.5
    )
    
    grados, activaciones, _, _, desvio_final = inferir_desvio(ocupacion_val)
    
    col_dif1, col_dif2 = st.columns([1, 2])
    with col_dif1:
        st.subheader("Métricas Difusas")
        st.metric(label="Desvío Recomendado (Centroide)", value=f"{desvio_final:.2f} %")
        
        st.markdown("**Grados de Pertenencia:**")
        for t, g in grados.items():
            st.write(f"- Ocupación **{t}**: `{g:.3f}`")
            
        st.markdown("**Activación de Reglas:**")
        for r, a in activaciones.items():
            st.write(f"- Regla **{r}**: `{a:.3f}`")
            
    with col_dif2:
        st.subheader("Funciones de Pertenencia")
        fig = generar_grafico_difuso(ocupacion_val)
        st.pyplot(fig)