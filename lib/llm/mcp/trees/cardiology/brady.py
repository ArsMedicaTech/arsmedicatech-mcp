"""
Bradycardia decision tree for determining appropriate management strategies.
"""

from typing import Any, Dict

BRADYCARDIA_MAIN_1_TREE: Dict[str, Any] = {
    "question": "Does the patient present with symptoms suggestive of or consistent with bradycardia or a conduction disorder?",
    "branches": {
        "== True": {
            "question": "After performing a comprehensive history, physical examination, ECG, and directed blood testing, what is the primary finding on the ECG?",
            "branches": {
                "== 'SND*'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                "== 'Nondiagnostic'": {
                    "question": "Is structural heart disease suspected based on history and physical examination?",
                    "branches": {
                        "== True": "OUTCOME: Perform Echocardiography.",
                        "== False": "OUTCOME: The ECG is nondiagnostic and structural heart disease is not suspected. Further clinical evaluation is required.",
                    },
                },
            },
        },
        "== False": "OUTCOME: This diagnostic algorithm is not applicable.",
    },
}

BRADYCARDIA_MAIN_2_TREE: Dict[str, Any] = {
    "question": "Does the patient have exercise-related symptoms?",
    "branches": {
        "== True": {
            "question": "What is the result of the Exercise ECG testing?",
            "branches": {
                "== 'Normal'": {
                    "question": "What are the findings from subsequent Ambulatory ECG monitoring?",
                    "branches": {
                        "== 'Significant arrhythmias'": {
                            "question": "What is the nature of the arrhythmia?",
                            "branches": {
                                "== 'SND'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                                "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                                "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                            },
                        },
                        "== 'No significant arrhythmias'": "OUTCOME: Observation. If concern for bradycardia continues, consider an Implantable Cardiac Monitor (ICM).",
                    },
                },
                "== 'Abnormal'": {
                    "question": "What is the nature of the abnormality?",
                    "branches": {
                        "== 'SND'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                        "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                        "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                    },
                },
            },
        },
        "== False": {
            "question": "Are the symptoms infrequent (e.g., occurring less than once every 30 days)?",
            "branches": {
                "== True": {
                    "question": "What are the findings from the Implantable Cardiac Monitor (ICM)?",
                    "branches": {
                        "== 'Significant arrhythmias'": {
                            "question": "What is the nature of the arrhythmia?",
                            "branches": {
                                "== 'SND'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                                "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                                "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                            },
                        },
                        "== 'No significant arrhythmias'": "OUTCOME: Observation. If concern for bradycardia continues, continue monitoring with ICM.",
                    },
                },
                "== False": {
                    "question": "What are the findings from Ambulatory ECG monitoring?",
                    "branches": {
                        "== 'Significant arrhythmias'": {
                            "question": "What is the nature of the arrhythmia?",
                            "branches": {
                                "== 'SND'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                                "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                                "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                            },
                        },
                        "== 'No significant arrhythmias'": "OUTCOME: Observation. If concern for bradycardia continues, consider an Implantable Cardiac Monitor (ICM).",
                    },
                },
            },
        },
    },
}
