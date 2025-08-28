"""
Atrial fibrillation (AFib) decision tree for determining appropriate management strategies.
"""

# ───────────────────────────────────────────────────────────
#  Atrial Fibrillation Decision Tree
#  (adapted from 2023 AHA/ACC/ACCP/HRS guideline)
# ───────────────────────────────────────────────────────────

from typing import Annotated, Any, Dict

from fastmcp import Context
from pydantic import Field

from lib.llm.mcp.mcp_init import mcp
from lib.llm.mcp.trees.common import decision_tree_lookup

ATRIAL_FIBRILLATION_TREE: Dict[str, Any] = {
    "question": "Hemodynamically stable?",
    "branches": {
        ("==", False): "Direct current cardioversion (1)",
        ("==", True): {
            "question": "Decompensated HF?",
            "branches": {
                ("==", False): {
                    "question": "Are beta blockers, verapamil, or diltiazem (1) contraindicated?",
                    "branches": {
                        ("==", False): "Continue current medications.",
                        ("==", True): {
                            "question": "Is Digoxin (2a) contraindicated?",
                            "branches": {
                                ("==", False): "Digoxin",
                                ("==", True): {
                                    "question": "Is Amiodarone (2b) contraindicated?",
                                    "branches": {
                                        ("==", False): "Amiodarone",
                                        ("==", True): "Consider alternative therapies.",
                                    },
                                },
                            },
                        },
                    },
                },
                ("==", True): {
                    "question": "Is IV Amiodarone (2b) contraindicated?",
                    "branches": {
                        ("==", False): "IV Amiodarone",
                        ("==", True): "That leaves Verapamil, diltiazem (3: Harm)",
                    },
                },
            },
        },
    },
}


@mcp.tool
def atrial_fibrillation_decision_tree_lookup(
    systolic_blood_pressure: Annotated[
        int, Field(description="The patient's systolic blood pressure, e.g., 128")
    ],
    diastolic_blood_pressure: Annotated[
        int, Field(description="The patient's diastolic blood pressure, e.g., 78")
    ],
    heart_rate: Annotated[int, Field(description="The patient's heart rate, e.g., 75")],
    decompensated_heart_failure: Annotated[
        bool, Field(description="Is the patient in decompensated heart failure?")
    ],
    beta_blockers_contraindicated: Annotated[
        bool,
        Field(
            description="Are beta blockers, verapamil, or diltiazem contraindicated?"
        ),
    ],
    digoxin_contraindicated: Annotated[
        bool, Field(description="Is Digoxin contraindicated?")
    ],
    amiodarone_contraindicated: Annotated[
        bool, Field(description="Is Amiodarone contraindicated?")
    ],
    ctx: Context,
) -> Dict[str, Any]:
    """
    Looks up a treatment recommendation for atrial fibrillation from a decision tree.

    Args:
        systolic_blood_pressure: The patient's systolic blood pressure.
        diastolic_blood_pressure: The patient's diastolic blood pressure.
        heart_rate: The patient's heart rate.
        decompensated_heart_failure: Is the patient in decompensated heart failure?
        beta_blockers_contraindicated: Are beta blockers, verapamil, or diltiazem contraindicated?
        digoxin_contraindicated: Is Digoxin contraindicated?
        amiodarone_contraindicated: Is Amiodarone contraindicated?
        ctx: The context for the lookup.

    Returns:
        A dictionary containing the final recommendation and the logical path taken.
    """
    # Implementation goes here
    pass


tool_definition_af: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "atrial_fibrillation_decision_tree_lookup",
        "description": "Looks up a treatment recommendation for atrial fibrillation from a decision tree.",
        "parameters": {
            "type": "object",
            "properties": {
                "ctx": {
                    "type": "object",
                    "description": "The context for the lookup.",
                },
            },
            "required": ["ctx"],
        },
    },
}
