"""
Example uses of decision tree functions.
"""

## EXAMPLE WITH INTEGER COMPARISONS ##

import enum
from typing import Any, Dict

from lib.llm.mcp.trees.common import decision_tree_lookup

LOAN_DECISION_TREE: Dict[str, Any] = {
    "question": "What is your credit score?",
    "branches": {
        ("<", 640): "Declined - Credit score too low",
        (">=", 640): {
            "question": "What is your annual income?",
            "branches": {
                ("<", 50000): {
                    "question": "What is the requested loan amount?",
                    "branches": {
                        ("<=", 10000): "Approved - Small loan with moderate income",
                        (">", 10000): "Declined - Loan amount too high for income",
                    },
                },
                (">=", 50000): "Approved - Strong income and credit score",
            },
        },
    },
}


def loan_decision_tree_lookup(
    credit_score: int, income: int, requested_amount: int
) -> Dict[str, Any]:
    """
    Looks up a loan decision from a deterministic decision tree.

    Args:
        credit_score: The applicant's credit score.
        income: The applicant's annual income.
        requested_amount: The amount of the loan being requested.

    Returns:
        A dictionary containing the final decision and the logical path taken.
    """
    return decision_tree_lookup(
        LOAN_DECISION_TREE,
        credit_score=credit_score,
        income=income,
        requested_amount=requested_amount,
    )


tool_definition: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "decision_tree_lookup",
        "description": "Determines loan eligibility and outcome by checking against a set of financial rules.",
        "parameters": {
            "type": "object",
            "properties": {
                "credit_score": {
                    "type": "integer",
                    "description": "The applicant's credit score, e.g., 720",
                },
                "income": {
                    "type": "integer",
                    "description": "The applicant's total annual income, e.g., 65000",
                },
                "requested_amount": {
                    "type": "integer",
                    "description": "The total amount of the loan requested by the applicant",
                },
            },
            "required": ["credit_score", "income", "requested_amount"],
        },
    },
}


# ────────────────────────────────────────────────────────────
# Example: using Enum + membership tests
# ────────────────────────────────────────────────────────────
class Purpose(enum.Enum):
    """
    Enum for loan purposes with descriptive values.
    """

    HOME = "home"
    CAR = "car"
    EDUCATION = "education"


ENHANCED_TREE: Dict[str, Any] = {
    "question": "What is the loan purpose?",
    "branches": {
        Purpose.HOME: "Declined - Mortgages not offered",
        Purpose.CAR: {
            "question": "What is your credit score?",
            "branches": {
                ("<", 600): "Declined - Credit too low for auto loan",
                (">=", 600): "Approved - Auto loan",
            },
        },
        Purpose.EDUCATION: {
            "question": "Which country is your university located in?",
            # sets must be hashable → use frozenset
            "branches": {
                ("in", frozenset({"US", "Canada"})): "Approved - Domestic study",
                ("not in", frozenset({"US", "Canada"})): "Declined - Foreign study",
            },
        },
    },
}


def enhanced_tree_lookup(
    purpose: Purpose, credit_score: int, country: str
) -> Dict[str, Any]:
    """
    Looks up a loan decision from an enhanced decision tree using Enum and membership tests.

    Args:
        purpose: The purpose of the loan (Purpose Enum).
        credit_score: The applicant's credit score.
        country: The country where the university is located.

    Returns:
        A dictionary containing the final decision and the logical path taken.
    """
    return decision_tree_lookup(
        ENHANCED_TREE, purpose=purpose, credit_score=credit_score, country=country
    )


tool_definition_enhanced: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "enhanced_tree_lookup",
        "description": "Determines loan eligibility and outcome by checking against a set of financial rules with enhanced features.",
        "parameters": {
            "type": "object",
            "properties": {
                "purpose": {
                    "type": "string",
                    "enum": [e.value for e in Purpose],
                    "description": "The purpose of the loan, e.g., 'home', 'car', 'education'",
                },
                "credit_score": {
                    "type": "integer",
                    "description": "The applicant's credit score, e.g., 720",
                },
                "country": {
                    "type": "string",
                    "description": "The country where the university is located, e.g., 'US', 'Canada'",
                },
            },
            "required": ["purpose", "credit_score", "country"],
        },
    },
}
