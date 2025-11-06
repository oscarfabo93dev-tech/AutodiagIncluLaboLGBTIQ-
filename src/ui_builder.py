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
    <div style="
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        color: #111827;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    ">
    
    ## Cuestionario de autodiagnóstico en inclusión laboral LGBTIQ+

    **Objetivo:** Este cuestionario permite evaluar, de forma rápida y estructurada, el nivel de madurez de su Agencia o Bolsa de Empleo en inclusión laboral de personas LGBTIQ+. Consta de 10 preguntas, cada una con tres opciones de respuesta que describen prácticas o situaciones concretas.

    ### ¿Cómo completarlo?
    1. Lea atentamente cada pregunta y sus tres opciones
    2. Seleccione la opción que mejor describa su situación actual
    3. Cada opción vale 3, 2 o 1 puntos (suma automática)
    4. Al finalizar, obtendrá su nivel: Inicial, Intermedio o Avanzado
    5. Recibirá una ruta de aprendizaje sugerida personalizada

    > **Confidencialidad:** Este autodiagnóstico es confidencial y está diseñado para uso interno como insumo para la mejora continua y la planificación estratégica en diversidad, equidad e inclusión.
    
    </div>
    """,
        unsafe_allow_html=True,
    )


# ---------- preguntas ----------


def _radio_for_question(q: Dict[str, Any], idx: int) -> Tuple[int, str]:
    """
    Render de una pregunta con diseño responsive mejorado.
    """
    # Sección arriba del enunciado
    section = q.get("section") or ""
    if section:
        st.markdown(
            f"""
            <div style="
                display: inline-block;
                font-size: 0.9rem;
                color: #6b7280;
                background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                border: 1px solid #d1d5db;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                margin: 0 0 0.75rem 0;
                font-weight: 600;
            ">
                {esc(section)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Enunciado responsive
    st.markdown(
        f"""
        <div style="
            font-size: clamp(1.1rem, 2.5vw, 1.4rem);
            line-height: 1.6;
            color: #111827;
            background-color: #ffffff;
            margin: 0.5rem 0 1rem 0;
            font-weight: 700;
            padding: 0.5rem 0;
        ">
            <span style="color: #667eea; font-weight: 800;">{esc(q.get('id', ''))}.</span> {esc(q.get('text', ''))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Opciones 3,2,1
    opts = sorted(q.get("options", []), key=lambda x: int(x["score"]), reverse=True)
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

    st.markdown(
        '<div style="height: 1.5rem; border-bottom: 1px solid #e5e7eb; margin: 1rem 0;"></div>',
        unsafe_allow_html=True,
    )

    if choice is not None:
        chosen = opts[choice]
        return int(chosen.get("score", 0)), str(chosen.get("label", ""))
    else:
        return 0, ""


def build_quiz_form(
    questions: List[Dict[str, Any]], show_missing_hint: bool = False
) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Pinta todas las preguntas con barra de progreso LGBTI.
    """
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
            st.warning(f"Falta responder la pregunta **{q.get('id','?')}**")

    # Barra de progreso con colores de la bandera LGBTI
    if len(questions) > 0:
        progress = completed_questions / len(questions)

        # Gradiente de la bandera LGBTI
        lgbti_gradient = "linear-gradient(to right, #E40303 0%, #FF8C00 16.67%, #FFED00 33.33%, #008026 50%, #24408E 66.67%, #732982 83.33%, #732982 100%)"

        st.markdown(
            f"""
            <div style="
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(to top, #ffffff 0%, rgba(255,255,255,0.98) 100%);
                padding: clamp(0.75rem, 2vw, 1.25rem);
                border-top: 2px solid #e5e7eb;
                box-shadow: 0 -4px 16px rgba(0,0,0,0.1);
                z-index: 999;
                backdrop-filter: blur(10px);
            ">
                <div style="max-width: 1200px; margin: 0 auto;">
                    <div style="
                        height: 14px;
                        background-color: #e5e7eb;
                        border-radius: 999px;
                        overflow: hidden;
                        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                    ">
                        <div style="
                            height: 100%;
                            width: {progress * 100}%;
                            background: {lgbti_gradient};
                            transition: width 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
                            box-shadow: 0 0 12px rgba(0,0,0,0.15);
                        "></div>
                    </div>
                    <div style="
                        margin-top: 0.5rem;
                        color: #374151;
                        font-size: clamp(0.85rem, 2vw, 1rem);
                        text-align: center;
                        font-weight: 600;
                    ">
                        {'Completado' if completed_questions == len(questions) else f'Progreso: {completed_questions}/{len(questions)} preguntas · Faltan {len(questions)-completed_questions}'}
                    </div>
                </div>
            </div>
            <div style="height: clamp(70px, 15vw, 90px);"></div>
            """,
            unsafe_allow_html=True,
        )

    return answers, labels


# ---------- resultados ----------


def show_result(
    result: Dict[str, Any],
    levels: Dict[str, Dict[str, str]],
    recommendations: pd.DataFrame,
    areas: Dict[str, int],
) -> None:
    # Encabezado responsive y centrado
    st.markdown(
        """
    <div style="
        max-width: 800px;
        margin: 2rem auto 1rem auto;
        text-align: center;
        background-color: #ffffff;
    ">
        <h2 style="
            color: #111827;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">
            Resultados del diagnóstico
        </h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Tarjeta principal responsive y centrada
    st.markdown(
        f"""
    <div style="
        max-width: 800px;
        margin: 1.5rem auto 2rem auto;
        padding: clamp(1.5rem, 4vw, 2.5rem);
        border-radius: 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.35);
        animation: fadeIn 0.5s ease;
    ">
        <div style="
            font-size: clamp(1.5rem, 4vw, 2rem);
            font-weight: 800;
            margin-bottom: 0.5rem;
        ">
            {esc(result['level_label'])}
        </div>
        <div style="
            font-size: clamp(1rem, 2.5vw, 1.3rem);
            font-weight: 600;
            opacity: 0.95;
        ">
            Puntaje total: {int(result['total'])} puntos
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    lv_key = result["level_key"]
    lv = levels.get(lv_key, {})

    # Cards más anchas y centradas
    def _card(title: str, color: str, text: str) -> None:
        st.markdown(
            f"""
            <div style="
                max-width: 800px;
                margin: 1.5rem auto;
                padding: clamp(1.25rem, 3vw, 2rem);
                border-radius: 12px;
                background: #ffffff;
                border: 2px solid {color}30;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            ">
                <div style="
                    color: {color};
                    font-weight: 700;
                    font-size: clamp(1.2rem, 2.5vw, 1.5rem);
                    margin-bottom: 1rem;
                    border-bottom: 3px solid {color};
                    width: fit-content;
                    padding-bottom: 0.35rem;
                    padding-right: 0.75rem;
                ">{esc(title)}</div>
                <div style="
                    line-height: 1.8;
                    color: #374151;
                    font-size: clamp(1rem, 2vw, 1.15rem);
                    background-color: #ffffff;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                ">
                    {esc(text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if lv:
        _card(
            "Definición",
            "#667eea",
            lv.get("DEFINICION", "(sin definición)"),
        )
        _card(
            "Características",
            "#764ba2",
            lv.get("CARACTERISTICAS", "(sin características)"),
        )
        _card(
            "Ruta de aprendizaje",
            "#28a745",
            lv.get("RUTA", "(sin ruta)"),
        )

    # Áreas a fortalecer - VERTICALES y centradas
    if areas:
        # Contenedor principal centrado
        st.markdown(
            """
        <div style="
            max-width: 800px;
            margin: 2.5rem auto 1.5rem auto;
            background-color: #ffffff;
        ">
            <h3 style="
                color:#111827;
                font-size: clamp(1.3rem, 3vw, 1.6rem);
                font-weight:700;
                margin:0 0 0.5rem 0;
            ">
                Áreas a fortalecer
            </h3>
            <div style="
                color:#6b7280;
                margin-bottom: 1.5rem;
                font-size: clamp(0.9rem, 2vw, 1rem);
            ">
                Secciones donde se eligieron opciones de puntaje bajo:
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Layout vertical (una card debajo de otra) - centrado
        for sec, sc in areas.items():
            st.markdown(
                f"""
            <div style="
                max-width: 800px;
                margin: 0 auto 0.75rem auto;
                padding: clamp(1rem, 2.5vw, 1.5rem);
                border-radius: 10px;
                background: linear-gradient(145deg, #fff3cd 0%, #ffeaa7 100%);
                border: 2px solid #f1c40f;
                box-shadow: 0 3px 12px rgba(241, 196, 15, 0.2);
                transition: transform 0.2s ease;
            ">
                <div style="
                    color:#7a5d00;
                    font-weight:700;
                    margin-bottom:0.5rem;
                    font-size: clamp(1rem, 2.2vw, 1.2rem);
                ">{esc(sec)}</div>
                <div style="
                    color:#7a5d00;
                    font-size: clamp(0.9rem, 1.9vw, 1rem);
                ">Puntaje ≤ {int(sc)}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Cerrar contenedor principal
        st.markdown("</div>", unsafe_allow_html=True)
