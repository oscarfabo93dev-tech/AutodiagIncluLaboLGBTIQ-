# app.py
# -*- coding: utf-8 -*-
import streamlit as st
import base64
from src.data_handler import load_data
from src.quiz_logic import calculate_score, sections_to_improve
from src.ui_builder import display_instructions, build_quiz_form, show_result

st.set_page_config(
    page_title="Autodiagnóstico LGBTIQ+",
    page_icon="🏳️‍🌈",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Función para cargar imágenes como base64
@st.cache_data
def get_image_base64(image_path: str) -> str:
    """Convierte imagen a base64 para embeber en HTML."""
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error cargando imagen {image_path}: {e}")
        return ""


# Cargar logos
logo1_base64 = get_image_base64("assets/cropped-Logo_WebSite.png")
logo2_base64 = get_image_base64("assets/camara-de-la-diversidad.jpg_1.png")

# CSS global con tema responsive mejorado - IDENTIDAD VISUAL COMPLETA
st.markdown(
    """
<style>
/* Variables de tema */
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --success-color: #28a745;
  --warning-color: #f1c40f;
  --danger-color: #dc3545;
  --text-dark: #111827;
  --text-light: #6b7280;
  --bg-white: #ffffff;
  --bg-light: #f8f9fa;
  --border-color: #e5e7eb;
  --button-discrete: #5a67d8;
}

/* Reset y base */
* {
  box-sizing: border-box;
}

/* Ocultar elementos de Streamlit innecesarios */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Contenedor principal responsive */
.main .block-container {
  max-width: 1200px;
  padding: 2rem 1rem;
}

/* Logos header responsive */
.logos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1000px;
  margin: 0 auto 2rem auto;
  padding: 1rem;
  gap: 2rem;
}

.logo-img {
  max-height: 80px;
  width: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.logo-img:hover {
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .logos-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .logo-img {
    max-height: 60px;
  }
}

/* Cards responsive */
.card {
  max-width: 1200px;
  margin: 1.5rem auto;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: linear-gradient(145deg, var(--bg-white) 0%, var(--bg-light) 100%);
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* Badge responsive */
.badge {
  margin-top: 0.8rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-light);
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--text-light);
  display: inline-block;
  transition: background-color 0.2s ease;
}

.badge:hover {
  background-color: #e5e7eb;
}

/* Botones mejorados */
.stButton > button {
  width: 100%;
  padding: 0.75rem 2rem !important;
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
  border: none !important;
  color: white !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
  transition: all 0.3s ease !important;
}

.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

.stButton > button:active {
  transform: translateY(0);
}

/* Radio buttons mejorados */
.stRadio > div {
  gap: 0.75rem;
}

.stRadio > div > label {
  padding: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 10px;
  background-color: var(--bg-white);
  cursor: pointer;
  transition: all 0.2s ease;
}

.stRadio > div > label:hover {
  border-color: var(--primary-color);
  background-color: #f3f4f6;
  transform: translateX(4px);
}

.stRadio > div > label[data-checked="true"] {
  border-color: var(--primary-color);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  font-weight: 600;
}

/* Expanders mejorados */
.streamlit-expanderHeader {
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  color: var(--text-dark) !important;
  background-color: var(--bg-light) !important;
  border-radius: 8px !important;
  padding: 1rem !important;
  transition: background-color 0.2s ease;
}

.streamlit-expanderHeader:hover {
  background-color: #e5e7eb !important;
}

/* Métricas mejoradas */
.stMetric {
  background-color: var(--bg-white);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Download button - discreto y ancho completo */
.stDownloadButton > button {
  width: 100%;
  padding: 0.75rem 2rem !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  background: linear-gradient(135deg, var(--button-discrete) 0%, #4c51bf 100%) !important;
  border: none !important;
  color: white !important;
  box-shadow: 0 4px 12px rgba(90, 103, 216, 0.25) !important;
  transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(90, 103, 216, 0.35) !important;
  background: linear-gradient(135deg, #4c51bf 0%, var(--button-discrete) 100%) !important;
}

/* Alerts centrados */
.stAlert {
  max-width: 800px;
  margin: 1rem auto !important;
}

/* Footer con logos */
.footer-logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  margin: 2rem auto 1rem auto;
  max-width: 800px;
  flex-wrap: wrap;
}

.footer-logo-img {
  max-height: 60px;
  width: auto;
  object-fit: contain;
  opacity: 0.8;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.footer-logo-img:hover {
  opacity: 1;
  transform: scale(1.05);
}

/* Responsive design */
@media (max-width: 768px) {
  .main .block-container {
    padding: 1rem 0.5rem;
  }
  
  .card {
    padding: 1.5rem;
    margin: 1rem 0;
  }
  
  .stButton > button,
  .stDownloadButton > button {
    font-size: 1rem !important;
    padding: 0.65rem 1.5rem !important;
  }
  
  h1 {
    font-size: 1.8rem !important;
  }
  
  h2 {
    font-size: 1.5rem !important;
  }
  
  h3 {
    font-size: 1.3rem !important;
  }
  
  .footer-logos {
    gap: 1.5rem;
  }
  
  .footer-logo-img {
    max-height: 50px;
  }
}

@media (max-width: 480px) {
  .main .block-container {
    padding: 0.75rem 0.25rem;
  }
  
  .card {
    padding: 1rem;
  }
  
  h1 {
    font-size: 1.5rem !important;
  }
  
  .footer-logo-img {
    max-height: 40px;
  }
}

/* Animaciones */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card, .stButton, .stRadio {
  animation: fadeIn 0.3s ease;
}

/* Scrollbar personalizado */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-light);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-color);
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Cargando datos del Excel...")
def load_cached_data():
    """Carga datos con caché para evitar recargas."""
    return load_data("data")


def main():
    # Header con logos
    if logo1_base64 and logo2_base64:
        st.markdown(
            f"""
            <div class="logos-header">
                <img src="data:image/png;base64,{logo1_base64}" class="logo-img" alt="Logo 1">
                <img src="data:image/png;base64,{logo2_base64}" class="logo-img" alt="Logo 2">
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Título con gradiente
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 style="
                color: var(--text-dark);
                font-size: 2.5rem;
                font-weight: 800;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Autodiagnóstico en inclusión laboral LGBTIQ+
            </h1>
            <p style="color: var(--text-light); font-size: 1.1rem; margin-top: 0.5rem;">
                Herramienta de evaluación para Agencias y Bolsas de Empleo
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Carga con caché
    data = load_cached_data()

    # Mostrar tiempos de carga (opcional, solo en debug)
    if "_load_timings" in data and st.sidebar.checkbox("Modo debug", value=False):
        with st.expander("Tiempos de carga (debug)", expanded=False):
            timings = data["_load_timings"]
            cols = st.columns(3)
            cols[0].metric("Total", f"{timings.get('total', 0):.2f}s")
            cols[1].metric("Cuestionario", f"{timings.get('cuestionario', 0):.3f}s")
            cols[2].metric("Niveles", f"{timings.get('niveles', 0):.3f}s")

    instructions = data["instructions"]
    questions = data["questions"]
    thresholds = data["thresholds"]
    levels = data["levels"]
    recommendations = data["recommendations"]

    # Instrucciones
    with st.expander("Ver instrucciones", expanded=True):
        display_instructions(instructions)

    # Formulario
    st.markdown("---")
    answers, labels = build_quiz_form(questions)

    # Botón centrado usando columnas simétricas
    calc_cols = st.columns([1, 2, 1])
    with calc_cols[1]:
        calc_clicked = st.button(
            "Calcular resultado", type="primary", use_container_width=True
        )

    if calc_clicked:
        total_q = len(questions)
        answered_q = len(answers)
        missing_q = total_q - answered_q

        if missing_q > 0:
            st.error(
                f"No has completado el cuestionario: faltan **{missing_q} pregunta(s)**. "
                "Responde todas antes de calcular."
            )
        else:
            # Calcula resultado
            res = calculate_score(answers, thresholds)
            areas = sections_to_improve(answers, questions)

            st.markdown("---")
            show_result(res, levels, recommendations, areas)

            # Generación de PDF
            from io import BytesIO
            from reportlab.lib.pagesizes import LETTER
            from reportlab.lib.units import inch
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

            def create_result_pdf(result, levels, areas_dict) -> bytes:
                buf = BytesIO()
                doc = SimpleDocTemplate(
                    buf,
                    pagesize=LETTER,
                    leftMargin=0.8 * inch,
                    rightMargin=0.8 * inch,
                    topMargin=0.8 * inch,
                    bottomMargin=0.8 * inch,
                )
                styles = getSampleStyleSheet()
                story = []

                story.append(
                    Paragraph(
                        "<b>Autodiagnóstico en inclusión laboral LGBTIQ+</b>",
                        styles["Title"],
                    )
                )
                story.append(Spacer(1, 10))
                story.append(
                    Paragraph(
                        f"<b>Resultado:</b> {result['level_label']} &nbsp;&nbsp; "
                        f"<b>Puntaje total:</b> {int(result['total'])}",
                        styles["Normal"],
                    )
                )
                story.append(Spacer(1, 14))

                lv = levels.get(result["level_key"], {})

                def sec(titulo: str, contenido: str):
                    story.append(Paragraph(f"<b>{titulo}</b>", styles["Heading2"]))
                    story.append(Spacer(1, 4))
                    story.append(
                        Paragraph(
                            (contenido or "(sin contenido)").replace("\n", "<br/>"),
                            styles["Normal"],
                        )
                    )
                    story.append(Spacer(1, 10))

                sec("Definición", lv.get("DEFINICION"))
                sec("Características", lv.get("CARACTERISTICAS"))
                sec("Ruta de aprendizaje", lv.get("RUTA"))

                if areas_dict:
                    story.append(
                        Paragraph("<b>Áreas a fortalecer</b>", styles["Heading2"])
                    )
                    story.append(Spacer(1, 4))
                    for sec_name, sc in areas_dict.items():
                        story.append(
                            Paragraph(
                                f"• {sec_name} (puntaje ≤ {int(sc)})",
                                styles["Normal"],
                            )
                        )
                    story.append(Spacer(1, 10))

                doc.build(story)
                pdf = buf.getvalue()
                buf.close()
                return pdf

            pdf_bytes = create_result_pdf(res, levels, areas)

            # Botón de descarga centrado
            dl_cols = st.columns([1, 2, 1])
            with dl_cols[1]:
                st.download_button(
                    label="Descargar PDF del resultado",
                    data=pdf_bytes,
                    file_name="resultado_autodiagnostico_lgbtiq.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

    # Footer con logos
    st.markdown("---")
    if logo1_base64 and logo2_base64:
        st.markdown(
            f"""
            <div class="footer-logos">
                <img src="data:image/png;base64,{logo1_base64}" class="footer-logo-img" alt="Logo 1">
                <img src="data:image/png;base64,{logo2_base64}" class="footer-logo-img" alt="Logo 2">
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="text-align: center; color: var(--text-light); font-size: 0.9rem; padding: 1rem 0;">
            <p>Desarrollado con compromiso por la inclusión | © 2025</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                Este diagnóstico es confidencial y está diseñado para uso interno
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
