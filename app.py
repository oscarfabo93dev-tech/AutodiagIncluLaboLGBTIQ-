# app.py
# -*- coding: utf-8 -*-
import streamlit as st
from src.data_handler import load_data
from src.quiz_logic import calculate_score, sections_to_improve
from src.ui_builder import display_instructions, build_quiz_form, show_result

st.set_page_config(page_title="Autodiagnóstico LGBTIQ+", layout="centered")

# CSS global para estilos reutilizables
st.markdown(
    """
<style>
.card {
  max-width: 1200px;
  margin: 1.5rem auto;
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.badge {
  margin-top: 0.8rem;
  padding: 0.5rem 0.75rem;
  background-color: #f1f3f4;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #5f6368;
  display: inline-block;
}
</style>
""",
    unsafe_allow_html=True,
)


def main():
    # 1) Título sin "(desde Excel)"
    st.title("Autodiagnóstico en inclusión laboral LGBTIQ+")

    # Carga directa desde data/
    data = load_data("data")

    instructions = data["instructions"]
    questions = data["questions"]
    thresholds = data["thresholds"]
    levels = data["levels"]
    recommendations = data["recommendations"]

    # Instrucciones
    with st.expander("Ver instrucciones", expanded=True):
        display_instructions(instructions)

    # Formulario
    answers, labels = build_quiz_form(questions)

    # 2) Validación y 3) PDF al finalizar
    if st.button("Calcular resultado", type="primary"):
        total_q = len(questions)
        answered_q = len(answers)
        missing_q = total_q - answered_q

        if missing_q > 0:
            st.error(
                f"No has completado el cuestionario: faltan {missing_q} pregunta(s). Responde todas antes de calcular."
            )
            # Opcional: re-render con hints visuales
            # _ = build_quiz_form(questions, show_missing_hint=True)
            return

        # Calcula resultado
        res = calculate_score(answers, thresholds)
        areas = sections_to_improve(answers, questions)
        show_result(res, levels, recommendations, areas)

        # ---- Generación de PDF (ReportLab) ----
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

            # Encabezado
            story.append(
                Paragraph(
                    "<b>Autodiagnóstico en inclusión laboral LGBTIQ+</b>",
                    styles["Title"],
                )
            )
            story.append(Spacer(1, 10))
            story.append(
                Paragraph(
                    f"<b>Resultado:</b> {result['level_label']} &nbsp;&nbsp; <b>Puntaje total:</b> {int(result['total'])}",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 14))

            # Secciones del nivel
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

            # Áreas a fortalecer
            if areas_dict:
                story.append(Paragraph("<b>Áreas a fortalecer</b>", styles["Heading2"]))
                story.append(Spacer(1, 4))
                for sec_name, sc in areas_dict.items():
                    story.append(
                        Paragraph(
                            f"• {sec_name} (puntaje ≤ {int(sc)})", styles["Normal"]
                        )
                    )
                story.append(Spacer(1, 10))

            doc.build(story)
            pdf = buf.getvalue()
            buf.close()
            return pdf

        pdf_bytes = create_result_pdf(res, levels, areas)
        st.download_button(
            label="Descargar PDF del resultado",
            data=pdf_bytes,
            file_name="resultado_autodiagnostico.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
