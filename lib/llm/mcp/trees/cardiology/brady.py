"""
Bradycardia decision tree for determining appropriate management strategies.
"""

from typing import Any, Dict

BRADYCARDIA_MAIN_1_TREE: Dict[str, Any] = {
    "question": "Does the patient present with symptoms suggestive of or consistent with bradycardia or a conduction disorder?",
    "branches": {
        ("==", True): {
            "question": "After performing a comprehensive history, physical examination, ECG, and directed blood testing, what is the primary finding on the ECG?",
            "variable": "ecg_finding",
            "branches": {
                "== 'SND*'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                "== 'Nondiagnostic'": {
                    "question": "Is structural heart disease suspected based on history and physical examination?",
                    "variable": "structural_heart_disease_suspected",
                    "branches": {
                        ("==", True): "OUTCOME: Perform Echocardiography.",
                        (
                            "==",
                            False,
                        ): "OUTCOME: The ECG is nondiagnostic and structural heart disease is not suspected. Further clinical evaluation is required.",
                    },
                },
            },
        },
        ("==", False): "OUTCOME: This diagnostic algorithm is not applicable.",
    },
}

BRADYCARDIA_MAIN_2_TREE: Dict[str, Any] = {
    "question": "Does the patient have exercise-related symptoms?",
    "branches": {
        ("==", True): {
            "question": "What is the result of the Exercise ECG testing?",
            "variable": "exercise_ecg_result",
            "branches": {
                "== 'Normal'": {
                    "question": "What are the findings from subsequent Ambulatory ECG monitoring?",
                    "variable": "ambulatory_ecg_findings",
                    "branches": {
                        "== 'Significant arrhythmias'": {
                            "question": "What is the nature of the arrhythmia?",
                            "variable": "arrhythmia_nature",
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
                    "variable": "abnormality_nature",
                    "branches": {
                        "== 'SND'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                        "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                        "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                    },
                },
            },
        },
        ("==", False): {
            "question": "Are the symptoms infrequent (e.g., occurring less than once every 30 days)?",
            "variable": "infrequent_symptoms",
            "branches": {
                ("==", True): {
                    "question": "What are the findings from the Implantable Cardiac Monitor (ICM)?",
                    "variable": "icm_findings",
                    "branches": {
                        "== 'Significant arrhythmias'": {
                            "question": "What is the nature of the arrhythmia?",
                            "variable": "arrhythmia_nature",
                            "branches": {
                                "== 'SND'": "OUTCOME: Proceed with the SND Diagnostic algorithm†.",
                                "== 'AV Block'": "OUTCOME: Proceed with the AV Block Diagnostic algorithm‡.",
                                "== 'Conduction disorder with 1:1 AV conduction'": "OUTCOME: Proceed with the Conduction disorder Diagnostic algorithm§.",
                            },
                        },
                        "== 'No significant arrhythmias'": "OUTCOME: Observation. If concern for bradycardia continues, continue monitoring with ICM.",
                    },
                },
                ("==", False): {
                    "question": "What are the findings from Ambulatory ECG monitoring?",
                    "variable": "ambulatory_ecg_findings",
                    "branches": {
                        "== 'Significant arrhythmias'": {
                            "question": "What is the nature of the arrhythmia?",
                            "variable": "arrhythmia_nature",
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

SND_TREE: Dict[str, Any] = {
    "question": "Is the sinus node dysfunction (SND) due to a reversible or physiologic cause?",
    "branches": {
        ("==", True): {
            "question": "After treating the underlying cause (Class I), is the treatment effective or unnecessary?",
            "variable": "treatment_effectiveness",
            "branches": {
                ("==", True): "OUTCOME: Observe.",
                ("==", False): {
                    "question": "Is there a suspicion for structural heart disease?",
                    "variable": "structural_heart_disease_suspected",
                    "branches": {
                        ("==", True): {
                            "question": "Following a transthoracic echocardiogram (Class IIa), is there suspicion for infiltrative cardiomyopathy, endocarditis, or adult congenital heart disease (ACHD)?",
                            "variable": "infiltrative_cardiomyopathy_suspected",
                            "branches": {
                                ("==", True): {
                                    "question": "After performing Advanced Imaging (Class IIa) and treating identified abnormalities, does the patient still have symptoms?",
                                    "variable": "persistent_symptoms",
                                    "branches": {
                                        ("==", True): {
                                            "question": "Are the symptoms exercise-related?",
                                            "variable": "exercise_related_symptoms",
                                            "branches": {
                                                ("==", True): {
                                                    "question": "Is the Exercise ECG testing (Class IIa) diagnostic?",
                                                    "variable": "exercise_ecg_result",
                                                    "branches": {
                                                        (
                                                            "==",
                                                            True,
                                                        ): "OUTCOME: Proceed to Sinus node dysfunction treatment algorithm‡.",
                                                        (
                                                            "==",
                                                            False,
                                                        ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                                    },
                                                },
                                                (
                                                    "==",
                                                    False,
                                                ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                            },
                                        },
                                        ("==", False): "OUTCOME: Observe.",
                                    },
                                },
                                ("==", False): {
                                    "question": "After treating any abnormalities identified on echo, does the patient still have symptoms?",
                                    "variable": "persistent_symptoms",
                                    "branches": {
                                        ("==", True): {
                                            "question": "Are the symptoms exercise-related?",
                                            "variable": "exercise_related_symptoms",
                                            "branches": {
                                                ("==", True): {
                                                    "question": "Is the Exercise ECG testing (Class IIa) diagnostic?",
                                                    "variable": "exercise_ecg_result",
                                                    "branches": {
                                                        (
                                                            "==",
                                                            True,
                                                        ): "OUTCOME: Proceed to Sinus node dysfunction treatment algorithm‡.",
                                                        (
                                                            "==",
                                                            False,
                                                        ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                                    },
                                                },
                                                (
                                                    "==",
                                                    False,
                                                ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                            },
                                        },
                                        ("==", False): "OUTCOME: Observe.",
                                    },
                                },
                            },
                        },
                        ("==", False): {
                            "question": "Does the patient have symptoms?",
                            "variable": "symptoms_present",
                            "branches": {
                                ("==", True): {
                                    "question": "Are the symptoms exercise-related?",
                                    "variable": "exercise_related_symptoms",
                                    "branches": {
                                        ("==", True): {
                                            "question": "Is the Exercise ECG testing (Class IIa) diagnostic?",
                                            "variable": "exercise_ecg_result",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Proceed to Sinus node dysfunction treatment algorithm‡.",
                                                (
                                                    "==",
                                                    False,
                                                ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                            },
                                        },
                                        (
                                            "==",
                                            False,
                                        ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                    },
                                },
                                ("==", False): "OUTCOME: Observe.",
                            },
                        },
                    },
                },
            },
        },
        ("==", False): {
            "question": "Is there a suspicion for structural heart disease?",
            "variable": "structural_heart_disease_suspected",
            "branches": {
                ("==", True): {
                    "question": "Following a transthoracic echocardiogram (Class IIa), is there suspicion for infiltrative cardiomyopathy, endocarditis, or adult congenital heart disease (ACHD)?",
                    "variable": "infiltrative_cardiomyopathy_suspected",
                    "branches": {
                        ("==", True): {
                            "question": "After performing Advanced Imaging (Class IIa) and treating identified abnormalities, does the patient still have symptoms?",
                            "variable": "persistent_symptoms",
                            "branches": {
                                ("==", True): {
                                    "question": "Are the symptoms exercise-related?",
                                    "variable": "exercise_related_symptoms",
                                    "branches": {
                                        ("==", True): {
                                            "question": "Is the Exercise ECG testing (Class IIa) diagnostic?",
                                            "variable": "exercise_ecg_result",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Proceed to Sinus node dysfunction treatment algorithm‡.",
                                                (
                                                    "==",
                                                    False,
                                                ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                            },
                                        },
                                        (
                                            "==",
                                            False,
                                        ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                    },
                                },
                                ("==", False): "OUTCOME: Observe.",
                            },
                        },
                        ("==", False): {
                            "question": "After treating any abnormalities identified on echo, does the patient still have symptoms?",
                            "variable": "persistent_symptoms",
                            "branches": {
                                ("==", True): {
                                    "question": "Are the symptoms exercise-related?",
                                    "variable": "exercise_related_symptoms",
                                    "branches": {
                                        ("==", True): {
                                            "question": "Is the Exercise ECG testing (Class IIa) diagnostic?",
                                            "variable": "exercise_ecg_result",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Proceed to Sinus node dysfunction treatment algorithm‡.",
                                                (
                                                    "==",
                                                    False,
                                                ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                            },
                                        },
                                        (
                                            "==",
                                            False,
                                        ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                    },
                                },
                                ("==", False): "OUTCOME: Observe.",
                            },
                        },
                    },
                },
                ("==", False): {
                    "question": "Does the patient have symptoms?",
                    "variable": "symptoms_present",
                    "branches": {
                        ("==", True): {
                            "question": "Are the symptoms exercise-related?",
                            "variable": "exercise_related_symptoms",
                            "branches": {
                                ("==", True): {
                                    "question": "Is the Exercise ECG testing (Class IIa) diagnostic?",
                                    "variable": "exercise_ecg_result",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Proceed to Sinus node dysfunction treatment algorithm‡.",
                                        (
                                            "==",
                                            False,
                                        ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                                    },
                                },
                                (
                                    "==",
                                    False,
                                ): "OUTCOME: Perform Ambulatory ECG monitoring (Class I), consider Electrophysiology study (Class IIb), and proceed to the SND treatment algorithm‡.",
                            },
                        },
                        ("==", False): "OUTCOME: Observe.",
                    },
                },
            },
        },
    },
}

AV_BLOCK_TREE: Dict[str, Any] = {
    "question": "Is the atrioventricular (AV) block due to a reversible or physiologic cause?",
    "branches": {
        ("==", True): {
            "question": "After treating the underlying cause (Class I), is the treatment effective or unnecessary?",
            "variable": "treatment_effective",
            "branches": {
                ("==", True): "OUTCOME: Observe.",
                ("==", False): {
                    "question": "Is the block a Mobitz Type II 2°, Advanced, or Complete Heart Block?",
                    "variable": "mobitz_type_ii_block",
                    "branches": {
                        ("==", True): {
                            "question": "Following a transthoracic echocardiogram (Class I), is there suspicion for infiltrative cardiomyopathy, endocarditis, or ACHD?",
                            "variable": "infiltrative_cardiomyopathy_suspected",
                            "branches": {
                                (
                                    "==",
                                    True,
                                ): "OUTCOME: Perform Advanced Imaging (Class IIa), then proceed to the AV block treatment algorithm†.",
                                (
                                    "==",
                                    False,
                                ): "OUTCOME: Proceed to the AV block treatment algorithm†.",
                            },
                        },
                        ("==", False): {
                            "question": "Is there a suspicion for structural heart disease?",
                            "variable": "structural_heart_disease_suspected",
                            "branches": {
                                ("==", True): {
                                    "question": "After performing an echocardiogram, treating abnormalities, and considering advanced imaging, what is the determined site of the AV Block?",
                                    "variable": "av_block_site",
                                    "branches": {
                                        "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                        "== 'AV node (Mobitz Type I)'": {
                                            "question": "Does the patient have symptoms?",
                                            "variable": "symptoms_present",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                ("==", False): "OUTCOME: Observe.",
                                            },
                                        },
                                        "== 'Unclear (e.g., 2:1 AV Block)'": {
                                            "question": "Does the patient have symptoms?",
                                            "variable": "symptoms_present",
                                            "branches": {
                                                ("==", True): {
                                                    "question": "What does the Electrophysiology study (Class IIb) show as the site of the block?",
                                                    "variable": "ep_study_result",
                                                    "branches": {
                                                        "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                        "== 'AV node'": "OUTCOME: Observe.",
                                                    },
                                                },
                                                ("==", False): {
                                                    "question": "What does Exercise testing (Class IIa) show as the site of the block?",
                                                    "variable": "exercise_ecg_result",
                                                    "branches": {
                                                        "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                        "== 'AV node'": "OUTCOME: Observe.",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                ("==", False): {
                                    "question": "What is the determined site of the AV Block?",
                                    "variable": "av_block_site",
                                    "branches": {
                                        "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                        "== 'AV node (Mobitz Type I)'": {
                                            "question": "Does the patient have symptoms?",
                                            "variable": "symptoms_present",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                ("==", False): "OUTCOME: Observe.",
                                            },
                                        },
                                        "== 'Unclear (e.g., 2:1 AV Block)'": {
                                            "question": "Does the patient have symptoms?",
                                            "variable": "symptoms_present",
                                            "branches": {
                                                ("==", True): {
                                                    "question": "What does the Electrophysiology study (Class IIb) show as the site of the block?",
                                                    "branches": {
                                                        "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                        "== 'AV node'": "OUTCOME: Observe.",
                                                    },
                                                },
                                                ("==", False): {
                                                    "question": "What does Exercise testing (Class IIa) show as the site of the block?",
                                                    "branches": {
                                                        "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                        "== 'AV node'": "OUTCOME: Observe.",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        ("==", False): {
            "question": "Is the block a Mobitz Type II 2°, Advanced, or Complete Heart Block?",
            "variable": "mobitz_type_ii_block",
            "branches": {
                ("==", True): {
                    "question": "Following a transthoracic echocardiogram (Class I), is there suspicion for infiltrative cardiomyopathy, endocarditis, or ACHD?",
                    "variable": "infiltrative_cardiomyopathy_suspected",
                    "branches": {
                        (
                            "==",
                            True,
                        ): "OUTCOME: Perform Advanced Imaging (Class IIa), then proceed to the AV block treatment algorithm†.",
                        (
                            "==",
                            False,
                        ): "OUTCOME: Proceed to the AV block treatment algorithm†.",
                    },
                },
                ("==", False): {
                    "question": "Is there a suspicion for structural heart disease?",
                    "variable": "structural_heart_disease_suspected",
                    "branches": {
                        ("==", True): {
                            "question": "After performing an echocardiogram, treating abnormalities, and considering advanced imaging, what is the determined site of the AV Block?",
                            "variable": "av_block_site",
                            "branches": {
                                "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                "== 'AV node (Mobitz Type I)'": {
                                    "question": "Does the patient have symptoms?",
                                    "variable": "symptoms_present",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                        ("==", False): "OUTCOME: Observe.",
                                    },
                                },
                                "== 'Unclear (e.g., 2:1 AV Block)'": {
                                    "question": "Does the patient have symptoms?",
                                    "variable": "symptoms_present",
                                    "branches": {
                                        ("==", True): {
                                            "question": "What does the Electrophysiology study (Class IIb) show as the site of the block?",
                                            "variable": "ep_study_result",
                                            "branches": {
                                                "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                "== 'AV node'": "OUTCOME: Observe.",
                                            },
                                        },
                                        ("==", False): {
                                            "question": "What does Exercise testing (Class IIa) show as the site of the block?",
                                            "variable": "exercise_ecg_result",
                                            "branches": {
                                                "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                "== 'AV node'": "OUTCOME: Observe.",
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        ("==", False): {
                            "question": "What is the determined site of the AV Block?",
                            "variable": "av_block_site",
                            "branches": {
                                "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                "== 'AV node (Mobitz Type I)'": {
                                    "question": "Does the patient have symptoms?",
                                    "variable": "symptoms_present",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                        ("==", False): "OUTCOME: Observe.",
                                    },
                                },
                                "== 'Unclear (e.g., 2:1 AV Block)'": {
                                    "question": "Does the patient have symptoms?",
                                    "variable": "symptoms_present",
                                    "branches": {
                                        ("==", True): {
                                            "question": "What does the Electrophysiology study (Class IIb) show as the site of the block?",
                                            "variable": "ep_study_result",
                                            "branches": {
                                                "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                "== 'AV node'": "OUTCOME: Observe.",
                                            },
                                        },
                                        ("==", False): {
                                            "question": "What does Exercise testing (Class IIa) show as the site of the block?",
                                            "variable": "exercise_ecg_result",
                                            "branches": {
                                                "== 'Infranodal'": "OUTCOME: Proceed to the AV block treatment algorithm†.",
                                                "== 'AV node'": "OUTCOME: Observe.",
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

ACUTE_BRADYCARDIA: Dict[str, Any] = {
    "question": "After an initial stability assessment and treatment of reversible causes, does the patient with acute bradycardia have moderate or severe symptoms?",
    "branches": {
        ("==", True): {
            "question": "After administration of Atropine, is the bradycardia suspected to be due to drug toxicity?",
            "variable": "drug_toxicity_suspected",
            "branches": {
                ("==", True): {
                    "question": "What is the suspected type of drug toxicity?",
                    "variable": "suspected_drug_toxicity",
                    "branches": {
                        "== 'Calcium channel blocker'": {
                            "question": "After administering IV Calcium (COR IIa) followed by High dose Insulin (COR IIa), do symptoms continue?",
                            "variable": "symptoms_present_after_iv_calcium",
                            "branches": {
                                ("==", True): {
                                    "question": "Is the patient now hemodynamically unstable or having severe symptoms?",
                                    "variable": "hemodynamic_instability",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                        ("==", False): {
                                            "question": "Is there a Myocardial Infarction (MI) with AV Block?",
                                            "variable": "av_block_site",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Administer Aminophylline (COR IIb), then proceed to Acute Pacing Algorithm‡.",
                                                ("==", False): {
                                                    "question": "After administering Beta-agonists (COR IIb), do symptoms continue?",
                                                    "variable": "symptoms_present",
                                                    "branches": {
                                                        (
                                                            "==",
                                                            True,
                                                        ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                                        (
                                                            "==",
                                                            False,
                                                        ): "OUTCOME: Symptoms resolved. Continue observation.",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                (
                                    "==",
                                    False,
                                ): "OUTCOME: Symptoms resolved. Continue observation.",
                            },
                        },
                        "== 'Beta blocker'": {
                            "question": "After administering IV Glucagon (COR IIa) followed by High dose Insulin (COR IIa), do symptoms continue?",
                            "variable": "symptoms_present",
                            "branches": {
                                ("==", True): {
                                    "question": "Is the patient now hemodynamically unstable or having severe symptoms?",
                                    "variable": "hemodynamic_instability",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                        ("==", False): {
                                            "question": "Is there a Myocardial Infarction (MI) with AV Block?",
                                            "variable": "av_block_site",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Administer Aminophylline (COR IIb), then proceed to Acute Pacing Algorithm‡.",
                                                ("==", False): {
                                                    "question": "After administering Beta-agonists (COR IIb), do symptoms continue?",
                                                    "variable": "symptoms_present",
                                                    "branches": {
                                                        (
                                                            "==",
                                                            True,
                                                        ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                                        (
                                                            "==",
                                                            False,
                                                        ): "OUTCOME: Symptoms resolved. Continue observation.",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                (
                                    "==",
                                    False,
                                ): "OUTCOME: Symptoms resolved. Continue observation.",
                            },
                        },
                        "== 'Digoxin'": {
                            "question": "After administering Anti-digoxin Fab (COR IIa), do symptoms continue?",
                            "variable": "symptoms_present_after_anti_digoxin_fab",
                            "branches": {
                                ("==", True): {
                                    "question": "Is the patient now hemodynamically unstable or having severe symptoms?",
                                    "variable": "hemodynamic_instability",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                        ("==", False): {
                                            "question": "Is there a Myocardial Infarction (MI) with AV Block?",
                                            "variable": "av_block_site",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Administer Aminophylline (COR IIb), then proceed to Acute Pacing Algorithm‡.",
                                                ("==", False): {
                                                    "question": "After administering Beta-agonists (COR IIb), do symptoms continue?",
                                                    "variable": "symptoms_present_after_beta_agonists",
                                                    "branches": {
                                                        (
                                                            "==",
                                                            True,
                                                        ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                                        (
                                                            "==",
                                                            False,
                                                        ): "OUTCOME: Symptoms resolved. Continue observation.",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                (
                                    "==",
                                    False,
                                ): "OUTCOME: Symptoms resolved. Continue observation.",
                            },
                        },
                    },
                },
                ("==", False): {
                    "question": "Do symptoms continue?",
                    "variable": "symptoms_present",
                    "branches": {
                        ("==", True): {
                            "question": "Is the patient now hemodynamically unstable or having severe symptoms?",
                            "variable": "hemodynamic_instability",
                            "branches": {
                                (
                                    "==",
                                    True,
                                ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                ("==", False): {
                                    "question": "Is there a Myocardial Infarction (MI) with AV Block?",
                                    "variable": "av_block_site",
                                    "branches": {
                                        (
                                            "==",
                                            True,
                                        ): "OUTCOME: Administer Aminophylline (COR IIb), then proceed to Acute Pacing Algorithm‡.",
                                        ("==", False): {
                                            "question": "After administering Beta-agonists (COR IIb), do symptoms continue?",
                                            "variable": "symptoms_present_after_beta_agonists",
                                            "branches": {
                                                (
                                                    "==",
                                                    True,
                                                ): "OUTCOME: Proceed to Acute Pacing Algorithm‡.",
                                                (
                                                    "==",
                                                    False,
                                                ): "OUTCOME: Symptoms resolved. Continue observation.",
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        (
                            "==",
                            False,
                        ): "OUTCOME: Symptoms resolved. Continue observation.",
                    },
                },
            },
        },
        ("==", False): "OUTCOME: Evaluation and observation.",
    },
}
