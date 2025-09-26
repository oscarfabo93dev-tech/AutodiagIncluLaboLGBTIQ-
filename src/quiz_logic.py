# src/quiz_logic.py
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, Any, List


def calculate_score(
    answers: Dict[str, int], thresholds: Dict[str, int]
) -> Dict[str, Any]:
    """
    Calcula puntaje total y nivel usando umbrales provistos (extraídos del Excel si fue posible).
    thresholds: {'nivel_1_max': 15, 'nivel_2_max': 23}
    """
    total = sum(int(v) for v in answers.values())
    n1 = int(thresholds.get("nivel_1_max", 15))
    n2 = int(thresholds.get("nivel_2_max", 23))

    if total <= n1:
        level_key = "Nivel 1"
        level_label = "Nivel 1 – Inicial"
    elif total <= n2:
        level_key = "Nivel 2"
        level_label = "Nivel 2 – Intermedio"
    else:
        level_key = "Nivel 3"
        level_label = "Nivel 3 – Avanzado"

    return {"total": total, "level_key": level_key, "level_label": level_label}


def sections_to_improve(
    answers: Dict[str, int], questions: List[Dict[str, Any]]
) -> Dict[str, int]:
    """
    Identifica secciones con respuestas <= 2, para orientar recomendaciones.
    Retorna {seccion: puntaje_min_detectado}
    """
    id_to_section = {q["id"]: q.get("section", "") for q in questions}
    secc_low: Dict[str, int] = {}
    for qid, score in answers.items():
        sec = id_to_section.get(qid, "General")
        s = int(score)
        if s <= 2:
            prev = secc_low.get(sec, 3)
            secc_low[sec] = min(prev, s)
    return secc_low
