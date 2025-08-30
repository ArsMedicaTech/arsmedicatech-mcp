"""
Blood pressure decision tree for classifying blood pressure levels and providing recommendations.
"""

import asyncio
from typing import Annotated, Any, Dict

from fastmcp import Context
from pydantic import Field

from lib.llm.mcp.trees.cardiology.afib import mcp
from lib.llm.mcp.trees.common import decision_tree_lookup
from settings import logger

# ───────────────────────────────────────────────────────────
#  Proof‑of‑concept decision tree: Blood‑pressure categories
#  (adapted from ACC/AHA 2017 guideline levels)
# ───────────────────────────────────────────────────────────

BP_DECISION_TREE: Dict[str, Any] = {
    "question": "What is your diastolic blood pressure?",
    "branches": {
        # Hypertensive crisis if DBP ≥120 mm Hg regardless of SBP
        (">=", 120): "Hypertensive crisis - Seek emergency care immediately",
        # Otherwise we still need SBP to finish the classification
        ("<", 120): {
            "question": "What is your systolic blood pressure?",
            "branches": {
                # Crisis if SBP ≥180 mm Hg (even though DBP <120)
                (">=", 180): "Hypertensive crisis - Seek emergency care immediately",
                # Hypertension Stage 2
                (
                    ">=",
                    140,
                ): "Hypertension Stage 2 - Discuss medication and lifestyle changes with a clinician",
                # Hypertension Stage 1
                (
                    "in",
                    range(130, 140),
                ): "Hypertension Stage 1 - Lifestyle changes and possible medication (clinician‑guided)",
                # Elevated BP (SBP 120‑129 *and* DBP < 80, which we already know here)
                (
                    "in",
                    range(120, 130),
                ): "Elevated blood pressure - Adopt heart‑healthy lifestyle",
                # Normal BP (SBP < 120 and DBP < 80)
                ("<", 120): "Normal blood pressure - Maintain current healthy habits",
            },
        },
    },
}


@mcp.tool
async def blood_pressure_decision_tree_lookup(
    systolic_blood_pressure: Annotated[
        int, Field(description="The patient's systolic blood pressure, e.g., 128")
    ],
    diastolic_blood_pressure: Annotated[
        int, Field(description="The patient's diastolic blood pressure, e.g., 78")
    ],
    ctx: Context,
) -> Dict[str, Any]:
    """
    Looks up a blood pressure classification from a decision tree.

    Args:
        systolic_blood_pressure: The patient's systolic blood pressure.
        diastolic_blood_pressure: The patient's diastolic blood pressure.

    Returns:
        A dictionary containing the final classification and the logical path taken.
    """
    # await ctx.info(f"Received systolic: {systolic_blood_pressure}, diastolic: {diastolic_blood_pressure}")
    logger.debug(
        f"Received systolic: {systolic_blood_pressure}, diastolic: {diastolic_blood_pressure}"
    )

    result = await asyncio.to_thread(
        decision_tree_lookup,
        BP_DECISION_TREE,
        **dict(
            systolic_blood_pressure=systolic_blood_pressure,
            diastolic_blood_pressure=diastolic_blood_pressure,
        ),
    )

    # await ctx.info("Lookup complete")
    logger.debug("Lookup complete")

    return result


tool_definition_bp: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "blood_pressure_decision_tree_lookup",
        "description": "Classifies blood pressure levels and provides recommendations based on systolic and diastolic values.",
        "parameters": {
            "type": "object",
            "properties": {
                "systolic_blood_pressure": {
                    "type": "integer",
                    "description": "The patient's systolic blood pressure, e.g., 128",
                },
                "diastolic_blood_pressure": {
                    "type": "integer",
                    "description": "The patient's diastolic blood pressure, e.g., 78",
                },
            },
            "required": ["systolic_blood_pressure", "diastolic_blood_pressure"],
        },
    },
}
