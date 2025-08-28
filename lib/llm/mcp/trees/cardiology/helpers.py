"""
Helper functions for cardiology-related decision trees.
"""


def mean_arterial_pressure(systolic: int, diastolic: int) -> float:
    """
    Calculates the mean arterial pressure (MAP) given systolic and diastolic blood pressure.

    Args:
        systolic: The systolic blood pressure.
        diastolic: The diastolic blood pressure.

    Returns:
        The mean arterial pressure.
    """
    return ((2 * diastolic) + systolic) / 3


def hemodynamic_stability(systolic: int, diastolic: int, heart_rate: int) -> bool:
    """
    Determines if the patient is hemodynamically stable based on the context.

    Args:
        systolic: The systolic blood pressure.
        diastolic: The diastolic blood pressure.
        heart_rate: The heart rate.

    Returns:
        True if the patient is hemodynamically stable, False otherwise.
    """
    hypotension = systolic < 90 or mean_arterial_pressure(systolic, diastolic) < 65
    tachycardia = heart_rate > 100
    shock_index = heart_rate / systolic

    return not hypotension and not tachycardia and shock_index < 0.7
