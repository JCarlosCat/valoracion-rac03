
import streamlit as st
import pandas as pd

# Lista donde se almacenan los registros temporalmente
if 'postulantes' not in st.session_state:
    st.session_state.postulantes = []

st.title("Valoración del Concurso de Méritos - RAC-03")
st.subheader("Ingreso de Datos del Postulante")

# --- Formulario ---
with st.form("formulario_meritos"):
    nombre = st.text_input("Nombre Completo")
    ci = st.text_input("Cédula de Identidad")
    asignatura = st.text_input("Asignatura")
    carrera = st.text_input("Carrera")

    st.markdown("### Estudios Académicos (máx. 1900)")
    licenciatura = st.number_input("Licenciatura", 0, 90)
    maestria = st.number_input("Maestría", 0, 300)
    doctorado = st.number_input("Doctorado", 0, 450)
    postdoctorado = st.number_input("Postdoctorado", 0, 400)
    estudios_total = licenciatura + maestria + doctorado + postdoctorado

    st.markdown("### Producción Intelectual (máx. 1000)")
    libros = st.number_input("Libros", 0, 300)
    articulos = st.number_input("Artículos Científicos", 0, 150)
    textos = st.number_input("Textos Académicos", 0, 200)
    guias = st.number_input("Guías o folletos", 0, 150)
    produccion_total = libros + articulos + textos + guias

    st.markdown("### Experiencia Docente (máx. 400)")
    docencia_emi = st.number_input("Docencia EMI", 0, 150)
    docencia_otras = st.number_input("Docencia otras universidades", 0, 100)
    docente_total = docencia_emi + docencia_otras

    st.markdown("### Experiencia Profesional (máx. 1000)")
    experiencia_prof = st.number_input("Años de experiencia profesional (x50)", 0, 20) * 50

    st.markdown("### Vida Universitaria (máx. 1000)")
    cargos = st.number_input("Cargos Académicos", 0, 1000)

    total = estudios_total + produccion_total + docente_total + experiencia_prof + cargos

    submitted = st.form_submit_button("Guardar Postulante")
    if submitted:
        st.session_state.postulantes.append({
            "Nombre": nombre,
            "CI": ci,
            "Asignatura": asignatura,
            "Carrera": carrera,
            "Estudios": estudios_total,
            "Producción Intelectual": produccion_total,
            "Experiencia Docente": docente_total,
            "Experiencia Profesional": experiencia_prof,
            "Vida Universitaria": cargos,
            "Total Puntos": total
        })
        st.success(f"Postulante {nombre} registrado con éxito.")

# --- Mostrar tabla ---
st.subheader("Postulantes Registrados")
df = pd.DataFrame(st.session_state.postulantes)
st.dataframe(df)

# --- Exportar a Excel ---
st.markdown("### Exportar a Excel")
if st.button("Descargar Excel"):
    df.to_excel("postulantes_rac03.xlsx", index=False)
    with open("postulantes_rac03.xlsx", "rb") as f:
        st.download_button("Haz clic para descargar", f, file_name="postulantes_rac03.xlsx")
