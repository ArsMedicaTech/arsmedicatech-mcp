"""
Atrial fibrillation (AFib) decision tree for determining appropriate management strategies.
"""

# ───────────────────────────────────────────────────────────
#  Atrial Fibrillation Decision Tree
#  (adapted from 2023 AHA/ACC/ACCP/HRS guideline)
# ───────────────────────────────────────────────────────────

from typing import Annotated, Any, Dict, Optional

from pydantic import Field

from lib.llm.mcp.mcp_init import mcp
from lib.llm.mcp.trees.cardiology.helpers import hemodynamic_stability_check
from lib.llm.mcp.trees.common import decision_tree_lookup

ATRIAL_FIBRILLATION_TREE: Dict[str, Any] = {
    "question": "Hemodynamically stable?",
    "variable": "hemodynamic_stability",
    "branches": {
        ("==", False): "Direct current cardioversion (1)",
        ("==", True): {
            "question": "Decompensated HF?",
            "variable": "decompensated_heart_failure",
            "branches": {
                ("==", False): {
                    "question": "Are beta blockers, verapamil, or diltiazem (1) contraindicated?",
                    "variable": "beta_blockers_contraindicated",
                    "branches": {
                        ("==", False): "Continue current medications.",
                        ("==", True): {
                            "question": "Is Digoxin (2a) contraindicated?",
                            "variable": "digoxin_contraindicated",
                            "branches": {
                                ("==", False): "Digoxin",
                                ("==", True): {
                                    "question": "Is Amiodarone (2b) contraindicated?",
                                    "variable": "amiodarone_contraindicated",
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
                    "variable": "amiodarone_contraindicated",
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
        Optional[int],
        Field(description="The patient's systolic blood pressure, e.g., 128"),
    ],
    diastolic_blood_pressure: Annotated[
        Optional[int],
        Field(description="The patient's diastolic blood pressure, e.g., 78"),
    ],
    heart_rate: Annotated[
        Optional[int], Field(description="The patient's heart rate, e.g., 75")
    ],
    hemodynamic_stability: Annotated[
        Optional[bool], Field(description="Is the patient hemodynamically stable?")
    ],
    decompensated_heart_failure: Annotated[
        bool, Field(description="Is the patient in decompensated heart failure?")
    ],
    beta_blockers_contraindicated: Annotated[
        bool,
        Field(description="Are beta blockers contraindicated?"),
    ],
    digoxin_contraindicated: Annotated[
        bool, Field(description="Is Digoxin contraindicated?")
    ],
    amiodarone_contraindicated: Annotated[
        bool, Field(description="Is Amiodarone contraindicated?")
    ],
) -> Dict[str, Any]:
    """
    Looks up a treatment recommendation for atrial fibrillation from a decision tree.

    Args:
        systolic_blood_pressure: The patient's systolic blood pressure.
        diastolic_blood_pressure: The patient's diastolic blood pressure.
        heart_rate: The patient's heart rate.
        hemodynamic_stability: Is the patient hemodynamically stable?
        decompensated_heart_failure: Is the patient in decompensated heart failure?
        beta_blockers_contraindicated: Are beta blockers contraindicated?
        digoxin_contraindicated: Is Digoxin contraindicated?
        amiodarone_contraindicated: Is Amiodarone contraindicated?

    Returns:
        A dictionary containing the final recommendation and the logical path taken.
    """
    if hemodynamic_stability is None and (
        systolic_blood_pressure is None
        and diastolic_blood_pressure is None
        and heart_rate is None
    ):
        raise ValueError(
            "If hemodynamic stability is unknown, all vital signs must be provided."
        )

    if not isinstance(hemodynamic_stability, bool):
        if (
            systolic_blood_pressure is None
            or diastolic_blood_pressure is None
            or heart_rate is None
        ):
            raise ValueError(
                "All vital signs (systolic_blood_pressure, diastolic_blood_pressure, heart_rate) must be provided to assess hemodynamic stability."
            )
        hemodynamic_stability_flag = hemodynamic_stability_check(
            systolic=systolic_blood_pressure,
            diastolic=diastolic_blood_pressure,
            heart_rate=heart_rate,
        )
    else:
        hemodynamic_stability_flag = hemodynamic_stability

    return decision_tree_lookup(
        ATRIAL_FIBRILLATION_TREE,
        hemodynamic_stability=hemodynamic_stability_flag,
        decompensated_heart_failure=decompensated_heart_failure,
        beta_blockers_contraindicated=beta_blockers_contraindicated,
        digoxin_contraindicated=digoxin_contraindicated,
        amiodarone_contraindicated=amiodarone_contraindicated,
    )


tool_definition_af: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "atrial_fibrillation_decision_tree_lookup",
        "description": "Looks up a treatment recommendation for atrial fibrillation from a decision tree.",
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
                "heart_rate": {
                    "type": "integer",
                    "description": "The patient's heart rate, e.g., 75",
                },
                "hemodynamic_stability": {
                    "type": ["boolean", "null"],
                    "description": "Is the patient hemodynamically stable?",
                },
                "decompensated_heart_failure": {
                    "type": "boolean",
                    "description": "Is the patient in decompensated heart failure?",
                },
                "beta_blockers_contraindicated": {
                    "type": "boolean",
                    "description": "Are beta blockers, verapamil, or diltiazem contraindicated?",
                },
                "digoxin_contraindicated": {
                    "type": "boolean",
                    "description": "Is Digoxin contraindicated?",
                },
                "amiodarone_contraindicated": {
                    "type": "boolean",
                    "description": "Is Amiodarone contraindicated?",
                },
            },
            "required": [
                "decompensated_heart_failure",
                "beta_blockers_contraindicated",
                "digoxin_contraindicated",
                "amiodarone_contraindicated",
            ],
        },
    },
}
