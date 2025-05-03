import streamlit as st
from fpdf import FPDF
import openai
import os

#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = ""
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_escape_room_description(course, sense, topic, num_students):
    prompt = f"""
    Genera un escape room educativo para {num_students} alumnos de {course} sobre el sentido matemático {sense} y la temática {topic}.
    El escape room debe seguir este formato:

    1. **Título:** Nombre atractivo del escape room.
    2. **Introducción:** Contexto narrativo de la historia.
    3. **Objetivo:** Qué deben lograr los estudiantes para escapar.
    4. **Materiales:** Listado de elementos necesarios para desarrollar la actividad.
    5. **Desarrollo:** Explicación detallada de la actividad dividida en:
       - **Reto 1:** Descripción y solución esperada.
       - **Reto 2:** Descripción y solución esperada.
       - **Reto 3:** Descripción y solución esperada.
    6. **Desenlace:** Qué ocurre cuando los estudiantes resuelven todos los retos.
    7. **Conclusión:** Reflexión educativa sobre la temática tratada.

    Asegúrate de que cada escape room generado tenga el mismo formato y sea claro y detallado.
    """

    with st.spinner("Generando Escape Room..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto en diseño de escape rooms educativos."},
                {"role": "user", "content": prompt}
            ]
        )

    return response["choices"][0]["message"]["content"].strip()

def save_as_pdf(text, filename="escape_room.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.image("logo_udima.png", x=10, y=8, w=33)  # Asegúrate de tener el logo en el mismo directorio
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Trabajo Fin de Máster", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Escape Room Matemático para Secundaria con IA", ln=True, align='C')
    pdf.cell(0, 10, "Autora: Alba Centeno Franco", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Escape Room Generado", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)
    return filename

def main():
    st.set_page_config(layout="wide")
    st.image("logo_udima.png", width=100)  # Asegúrate de tener el logo en el mismo directorio
    st.title("Escape Room Matemático para Secundaria con IA")
    st.markdown("**Autora: Alba Centeno Franco**")

    with st.sidebar:
        st.header("Configuración del Escape Room")
        course = st.selectbox("Selecciona el curso:", ["1º ESO", "2º ESO", "3º ESO", "4º ESO"])

        list_of_senses = ["Sentido numérico", "Sentido de la medida", "Sentido espacial", "Sentido algebraico", "Sentido estocástico"]
        senses = {
            "1º ESO": list_of_senses,
            "2º ESO": list_of_senses,
            "3º ESO": list_of_senses,
            "4º ESO": list_of_senses
        }
        sense = st.selectbox("Selecciona el sentido matemático:", senses[course])

        topics = {
            "1º ESO": {
                "Sentido numérico": ["Conteo y razonamiento proporcional", "Números racionales", "Operaciones numéricas"],
                "Sentido de la medida": ["Unidades de medida", "Estimación y cálculo de áreas", "Problemas de Fermi"],
                "Sentido espacial": ["Figuras geométricas planas", "Uso de herramientas digitales", "Congruencia"],
                "Sentido algebraico": ["Introducción al álgebra", "Generalización de patrones", "Ecuaciones sencillas"],
                "Sentido estocástico": ["Gráficos estadísticos", "Medidas de localización", "Probabilidad básica"]
            },
            "2º ESO": {
                "Sentido numérico": ["Fracciones y decimales", "Razonamiento proporcional avanzado"],
                "Sentido de la medida": ["Medida indirecta", "Relaciones métricas"],
                "Sentido espacial": ["Transformaciones geométricas", "Relaciones espaciales"],
                "Sentido algebraico": ["Funciones lineales", "Ecuaciones más complejas"],
                "Sentido estocástico": ["Inferencia estadística", "Comparación de distribuciones"]
            },
            "3º ESO": {
                "Sentido numérico": ["Potencias y raíces", "Logaritmos"],
                "Sentido de la medida": ["Trigonometría aplicada", "Tasas de variación"],
                "Sentido espacial": ["Trigonometría en el espacio", "Relaciones métricas"],
                "Sentido algebraico": ["Funciones cuadráticas", "Sistemas de ecuaciones"],
                "Sentido estocástico": ["Probabilidad condicional", "Combinatoria"]
            },
            "4º ESO": {
                "Sentido numérico": ["Números complejos", "Progresiones"],
                "Sentido de la medida": ["Optimización", "Tasas de variación avanzadas"],
                "Sentido espacial": ["Coordenadas en el espacio", "Transformaciones avanzadas"],
                "Sentido algebraico": ["Matrices y determinantes", "Funciones logarítmicas"],
                "Sentido estocástico": ["Inferencia estadística avanzada", "Regresión lineal"]
            }
        }
        topic = st.selectbox("Selecciona la temática:", topics[course][sense])

        num_students = st.number_input("Número de alumnos en la clase:", min_value=1, max_value=50, value=20)

        if st.button("Generar Escape Room"):
            st.session_state["generating"] = True
            st.session_state.pop("escape_room_text", None)
            escape_room_text = get_escape_room_description(course, sense, topic, num_students)
            st.session_state["escape_room_text"] = escape_room_text
            st.session_state["generating"] = False

        if st.button("Guardar Escape Room como PDF") and "escape_room_text" in st.session_state:
            filename = save_as_pdf(st.session_state["escape_room_text"])
            with open(filename, "rb") as file:
                st.download_button(label="Descargar PDF", data=file, file_name=filename, mime="application/pdf")

    with st.container():
        st.subheader("Escape Room Generado")
        with st.expander("Ver Escape Room generado", expanded=True):
            if "generating" in st.session_state and st.session_state["generating"]:
                st.info("Generando Escape Room...")
            elif "escape_room_text" in st.session_state:
                st.markdown(st.session_state["escape_room_text"])

if __name__ == "__main__":
    main()