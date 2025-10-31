# src/ui_builder.py
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import streamlit as st
import pandas as pd
import html
from uuid import uuid4

# ---------- util ----------


def esc(x: str) -> str:
    """Escapa HTML cuando usamos unsafe_allow_html=True."""
    return html.escape(x or "", quote=True)


def display_instructions(instructions_text: str) -> None:
    st.markdown(
        """
    ## Cuestionario de autodiagnóstico en inclusión laboral LGBTIQ+ (Agencias y Bolsas de Empleo)

    **Objetivo.** Este cuestionario permite evaluar, de forma rápida y estructurada, el nivel de madurez de su Agencia o Bolsa de Empleo en inclusión laboral de personas LGBTIQ+. Consta de **10 preguntas**, cada una con **tres opciones de respuesta** que describen prácticas o situaciones concretas.

    ### ¿Cómo completarlo?
    1. **Lea** atentamente cada pregunta y sus tres opciones.  
    2. **Seleccione** en la columna **"Respuesta"** la opción que mejor describa la situación actual de su Agencia.  
    3. **Puntajes:** cada opción equivale a **3, 2 o 1** puntos; la suma es **automática**.  
    4. Al finalizar, el **puntaje total** ubicará a su agencia o bolsa de empleo en uno  de los **tres niveles**: **Inicial**, **Intermedio** o **Avanzado**.  
    5. Según el nivel, el sistema mostrará una **ruta de aprendizaje sugerida** con talleres y acciones formativas para fortalecer sus prácticas (consulte las **pestañas** correspondientes en este documento).

    > **Confidencialidad.** Este autodiagnóstico es **confidencial** y está diseñado para uso **interno** como insumo para la mejora continua y la planificación estratégica en **diversidad, equidad e inclusión**.
    """
    )


# ---------- preguntas ----------


def _radio_for_question(q: Dict[str, Any], idx: int) -> Tuple[int, str]:
    """
    Render de una pregunta con la sección ENCIMA del enunciado.
    - La sección (si existe) aparece ARRIBA como una nota sutil.
    - Enunciado en tipografía prominente.
    - Radios 3/2/1 en vertical.
    """
    # Sección arriba del enunciado (sutil, gris claro)
    section = q.get("section") or ""
    if section:
        st.markdown(
            f"""
            <div style="
                display: inline-block;
                font-size: 0.95rem;
                color: #6b7280;         /* gris 500 */
                background: #f3f4f6;    /* gris 100 */
                border: 1px solid #e5e7eb; /* gris 200 */
                padding: 0.35rem 0.6rem;
                border-radius: 6px;
                margin: 0 0 0.5rem 0;   /* margen inferior para separar del enunciado */
            ">
                {esc(section)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Enunciado
    st.markdown(
        f"""
        <div style="
            font-size: 1.35rem;
            line-height: 1.6;
            color: #111827;        /* gris 900 */
            margin: 0.25rem 0 0.25rem 0;
            font-weight: 700;
        ">
            {esc(q.get('text', ''))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Opciones 3,2,1
    opts = sorted(q.get("options", []), key=lambda x: int(x["score"]), reverse=True)
    # Mostrar solo el texto de la opción (sin "(Puntuación: X)")
    labels = [esc(str(o.get("label", ""))) for o in opts]

    choice = st.radio(
        f"Seleccione una opción para la pregunta {esc(q.get('id',''))}:",
        options=list(range(len(opts))),
        format_func=lambda i: labels[i],
        index=None,
        key=f"q_{q.get('id','')}_{idx}_{st.session_state.get('_render_uid','0')}",
        horizontal=False,
        label_visibility="collapsed",
    )

    st.markdown('<div style="height: 1.0rem;"></div>', unsafe_allow_html=True)

    if choice is not None:
        chosen = opts[choice]
        return int(chosen.get("score", 0)), str(chosen.get("label", ""))
    else:
        return 0, ""


def build_quiz_form(
    questions: List[Dict[str, Any]], show_missing_hint: bool = False
) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Pinta todas las preguntas. Añade barra de progreso sticky (sin mover tu botón).
    """
    # Unique render id to avoid duplicate Streamlit keys when re-rendering with hints
    _ = st.session_state.setdefault("_render_uid", str(uuid4()))

    answers: Dict[str, int] = {}
    labels: Dict[str, str] = {}
    completed_questions = 0

    for idx, q in enumerate(questions):
        score, label = _radio_for_question(q, idx)
        if score > 0:
            answers[q["id"]] = score
            labels[q["id"]] = label
            completed_questions += 1
        elif show_missing_hint:
            st.warning(f"Falta responder la pregunta {q.get('id','?')}.", icon="⚠️")

    # ---- Sticky footer: SOLO barra de progreso (mantén tu botón en app.py) ----
    if len(questions) > 0:
        progress = completed_questions / len(questions)
        st.markdown(
            f"""
            <div style="
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: #ffffff;
                padding: 0.9rem 1.25rem;
                border-top: 1px solid #e5e7eb;
                box-shadow: 0 -4px 12px rgba(0,0,0,0.08);
                z-index: 999;
            ">
                <div style="max-width: 1200px; margin: 0 auto;">
                    <div style="
                        height: 10px;
                        background-color: #e5e7eb;
                        border-radius: 999px;
                        overflow: hidden;
                    ">
                        <div style="
                            height: 100%;
                            width: {progress * 100}%;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            transition: width 0.25s ease;
                        "></div>
                    </div>
                    <div style="margin-top: 0.4rem; color: #6b7280; font-size: 0.92rem; text-align:center;">
                            Progreso: {completed_questions} de {len(questions)} preguntas completadas{'' if completed_questions==len(questions) else f' · Te faltan {len(questions)-completed_questions}'}
                    </div>
                </div>
            </div>
            <div style="height: 80px;"></div>  <!-- espaciador para que el contenido no quede tapado -->
            """,
            unsafe_allow_html=True,
        )

    return answers, labels


# ---------- resultados ----------


def show_result(
    result: Dict[str, Any],
    levels: Dict[str, Dict[str, str]],
    recommendations: pd.DataFrame,  # se ignora (por solicitud), pero mantenemos la firma pública
    areas: Dict[str, int],
) -> None:
    # Encabezado del bloque de resultados
    st.markdown(
        """
    <div style="max-width: 1200px; margin: 2rem auto 0.5rem auto; text-align: center;">
        <h2 style="color: #111827; font-size: 2.1rem; font-weight: 700; margin: 0;">
            Resultados del diagnóstico
        </h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Tarjeta principal con gradiente (misma gama)
    st.markdown(
        f"""
    <div style="
        max-width: 900px;
        margin: 1rem auto 2rem auto;
        padding: 2.2rem;
        border-radius: 14px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.30);
    ">
        <div style="font-size: 1.8rem; font-weight: 800; margin-bottom: 0.35rem;">
            {esc(result['level_label'])}
        </div>
        <div style="font-size: 1.15rem; font-weight: 500; opacity: 0.95;">
            Puntaje total: {int(result['total'])}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    lv_key = result["level_key"]
    lv = levels.get(lv_key, {})

    # Bloques apilados (no columnas)
    def _card(title: str, color: str, text: str) -> None:
        st.markdown(
            f"""
            <div style="
                max-width: 1000px;
                margin: 1.1rem auto;
                padding: 1.25rem 1.35rem;
                border-radius: 10px;
                background: #ffffff;
                border: 1px solid #e5e7eb;
                box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            ">
                <div style="
                    color: {color};
                    font-weight: 700;
                    font-size: 1.2rem;
                    margin-bottom: 0.6rem;
                    border-bottom: 3px solid {color};
                    width: fit-content;
                    padding-bottom: 0.15rem;
                ">{esc(title)}</div>
                <div style="line-height: 1.65; color: #374151; font-size: 1.05rem;">
                    {esc(text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if lv:
        _card("Definición", "#667eea", lv.get("DEFINICION", "(sin definición)"))
        _card(
            "Características",
            "#764ba2",
            lv.get("CARACTERISTICAS", "(sin características)"),
        )
        _card("Ruta de aprendizaje", "#28a745", lv.get("RUTA", "(sin ruta)"))

    # Áreas a fortalecer
    if areas:
        st.markdown(
            """
        <div style="max-width: 1000px; margin: 2rem auto 0.5rem auto;">
            <h3 style="color:#111827; font-size:1.45rem; font-weight:700; margin:0 0 0.75rem 0;">
                Áreas a fortalecer
            </h3>
            <div style="color:#6b7280; margin-bottom: 0.75rem;">
                Secciones donde se eligieron opciones 1 o 2:
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    cols = st.columns(3)
    for i, (sec, sc) in enumerate(areas.items()):
        with cols[i % 3]:
            st.markdown(
                f"""
            <div style="
                padding: 0.9rem 1rem;
                margin: 0.4rem 0;
                border-radius: 8px;
                background: linear-gradient(145deg, #fff3cd 0%, #ffeaa7 100%);
                border: 1px solid #f1c40f;
                box-shadow: 0 2px 8px rgba(241, 196, 15, 0.18);
            ">
                <div style="color:#7a5d00; font-weight:700; margin-bottom:0.15rem;">{esc(sec)}</div>
                <div style="color:#7a5d00; font-size:0.92rem;">Puntaje ≤ {int(sc)}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
