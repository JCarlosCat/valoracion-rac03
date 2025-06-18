import streamlit as st
import pandas as pd
import io
from openpyxl import Workbook

# Inicializar la lista de postulantes si no existe
if 'postulantes' not in st.session_state:
    st.session_state.postulantes = []

st.title("Evaluación de Méritos - Concurso Docente RAC-03")

with st.form("formulario_postulante"):
    st.subheader("Datos Generales del Postulante")
    carrera = st.text_input("Carrera")
    ci = st.text_input("Cédula de Identidad")
    celular = st.text_input("Celular")
    apellido_paterno = st.text_input("Apellido Paterno")
    apellido_materno = st.text_input("Apellido Materno")
    nombres = st.text_input("Nombres")
    asignatura = st.text_input("Asignatura")
    semestre = st.text_input("Semestre de la Asignatura")
    cumple_requisitos = st.selectbox("¿Cumple Requisitos de la Convocatoria?", ["SI", "NO"])

    st.markdown("### Estudios Académicos (Máx. 1900 pts)")
    titulo_nacional = st.selectbox("¿Título en Provisión Nacional?", ["SI", "NO"])
    especialidad = st.text_input("Especialidad (ej. Ing. en Estadística)")
    universidad = st.text_input("Universidad")
    anio_titulacion = st.text_input("Año de Titulación")

    # Licenciatura
    tiene_licenciatura = st.checkbox("¿Tiene Licenciatura?")
    puntos_licenciatura = 60
    puntos_licenciatura_adicional = 30

    # Maestrías
    tiene_maestria = st.checkbox("¿Tiene Maestría?")
    cantidad_maestrias = st.number_input("¿Cuántas maestrías?", 0, 5, 0)
    puntos_maestria = 0
    if cantidad_maestrias > 0:
        puntos_maestria += 200
        puntos_maestria += 100 * (cantidad_maestrias - 1)

    # Doctorados
    tiene_doctorado = st.checkbox("¿Tiene Doctorado?")
    cantidad_doctorados = st.number_input("¿Cuántos doctorados?", 0, 3, 0)
    puntos_doctorado = 0
    if cantidad_doctorados > 0:
        puntos_doctorado += 300
        puntos_doctorado += 150 * (cantidad_doctorados - 1)

    # Postdoctorado
    tiene_postdoc = st.checkbox("¿Tiene Postdoctorado?")
    cantidad_postdoc = st.number_input("¿Cuántos postdoctorados?", 0, 3, 0)
    puntos_postdoc = 400 * cantidad_postdoc

    # Cálculo total
    total_estudios = 0
    if tiene_licenciatura:
        total_estudios += puntos_licenciatura + puntos_licenciatura_adicional
    total_estudios += puntos_maestria
    total_estudios += puntos_doctorado
    total_estudios += puntos_postdoc
    if total_estudios > 1900:
        total_estudios = 1900  # Límite del Art. 29

    st.success(f"Puntaje total en Estudios Académicos: {total_estudios} / 1900")

    submitted = st.form_submit_button("Guardar Postulante")
    if submitted:
        st.session_state.postulantes.append({
            "CARRERA": carrera,
            "CI": ci,
            "CEL": celular,
            "AP. PATERNO": apellido_paterno,
            "AP. MATERNO": apellido_materno,
            "NOMBRES": nombres,
            "ASIGNATURA": asignatura,
            "SEMESTRE": semestre,
            "FILTRO CONVOCATORIA": cumple_requisitos,
            "TÍTULO EN PROVISIÓN NACIONAL": titulo_nacional,
            "ESPECIALIDAD": especialidad,
            "UNIVERSIDAD": universidad,
            "AÑO DE TITULACIÓN": anio_titulacion,
            "PTJE. ESTUDIOS ACADÉMICOS": total_estudios
        })
        st.success(f"Postulante {nombres} registrado con éxito.")

# Mostrar tabla
st.subheader("Postulantes Registrados")
df = pd.DataFrame(st.session_state.postulantes)
st.dataframe(df)

# Exportar a Excel en memoria (funciona en Streamlit Cloud)
if st.button("Descargar Excel"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Postulantes')
    output.seek(0)
    st.download_button(
        label="Haz clic para descargar",
        data=output,
        file_name="evaluacion_meritos_rac03.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )





