"""
Bayesian API tools for MCP server - Bayesian inference for medical models.
"""
from typing import Any, Dict, List, Optional

import requests

from settings import logger

# API Configuration
URL_BASE = 'https://demo.arsmedicatech.com'
# URL_BASE = 'http://localhost:62295'  # For local development

# Model schemas - define the expected data structure for each model
MODEL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "sepsis": {
        "description": "Sepsis prediction model",
        "required_fields": ["temp", "hr", "wbc"],
        "optional_fields": ["systolic_bp", "diastolic_bp", "respiratory_rate"],
        "field_descriptions": {
            "temp": "Temperature in Celsius",
            "hr": "Heart rate in beats per minute",
            "wbc": "White blood cell count in K/μL",
            "systolic_bp": "Systolic blood pressure in mmHg",
            "diastolic_bp": "Diastolic blood pressure in mmHg",
            "respiratory_rate": "Respiratory rate in breaths per minute"
        },
        "field_types": {
            "temp": float,
            "hr": int,
            "wbc": float,
            "systolic_bp": int,
            "diastolic_bp": int,
            "respiratory_rate": int
        }
    }
    # Add more models here as they become available
}


def call_bayesian_model(model: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generic function to call any Bayesian model with arbitrary data.
    
    Args:
        model: Name of the Bayesian model to use
        data: Dictionary containing the model input data
    
    Returns:
        Dictionary containing the Bayesian inference results
    """
    try:
        # Validate model exists
        if model not in MODEL_SCHEMAS:
            model_schemas_str = ", ".join([str(k) for k in MODEL_SCHEMAS.keys()])
            return {
                "error": f"Unknown model '{model}'. Available models: {model_schemas_str}",
                "status": "error"
            }
        
        # Validate required fields
        schema: Dict[str, Any] = MODEL_SCHEMAS[model] # type: ignore
        missing_fields: List[str] = []
        for field in schema["required_fields"]:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "error": f"Missing required fields for model '{model}': {missing_fields}",
                "status": "error"
            }
        
        # Validate data types
        type_errors: List[str] = []
        for field, value in data.items():
            if field in schema["field_types"]:
                # error: Value of type "Collection[str]" is not indexable
                expected_type: type = schema["field_types"][field]
                if not isinstance(value, expected_type):
                    type_errors.append(
                        f"Field '{field}' should be {getattr(expected_type, '__name__', str(expected_type))}, got {type(value).__name__}"
                    )
        
        if type_errors:
            return {
                "error": f"Type validation errors: {type_errors}",
                "status": "error"
            }
        
        # Make API call
        url = f"{URL_BASE}/bayesian/models/{model}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "status": "success",
                "model": model,
                "data": data,
                "result": result
            }
        elif response.status_code == 503:
            return {
                "error": "Service Unavailable. Please try again later.",
                "status": "error",
                "model": model
            }
        else:
            return {
                "error": f"API Error: {response.status_code} - {response.text}",
                "status": "error",
                "model": model
            }
        
    except requests.RequestException as e:
        logger.error(f"Request error in Bayesian model call: {e}")
        return {
            "error": f"Request failed: {str(e)}",
            "status": "error",
            "model": model
        }
    except Exception as e:
        logger.error(f"Error in Bayesian model call: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "model": model
        }


def predict_sepsis(
    temp: float,
    hr: int,
    wbc: float,
    systolic_bp: Optional[int] = None,
    diastolic_bp: Optional[int] = None,
    respiratory_rate: Optional[int] = None
) -> Dict[str, Any]:
    """
    Predict sepsis probability using the Bayesian sepsis model.
    
    Args:
        temp: Temperature in Celsius
        hr: Heart rate in beats per minute
        wbc: White blood cell count in K/μL
        systolic_bp: Optional systolic blood pressure in mmHg
        diastolic_bp: Optional diastolic blood pressure in mmHg
        respiratory_rate: Optional respiratory rate in breaths per minute
    
    Returns:
        Dictionary containing sepsis prediction results
    """
    # Validate required parameters
    if not temp or not hr or not wbc:
        return {
            "error": "Temperature, heart rate, and WBC are required parameters",
            "status": "error"
        }
    
    # Prepare data dictionary
    data: Dict[str, Any] = {
        "temp": temp,
        "hr": hr,
        "wbc": wbc
    }
    
    # Add optional parameters if provided
    if systolic_bp is not None:
        data["systolic_bp"] = systolic_bp
    if diastolic_bp is not None:
        data["diastolic_bp"] = diastolic_bp
    if respiratory_rate is not None:
        data["respiratory_rate"] = respiratory_rate
    
    return call_bayesian_model("sepsis", data)


def get_available_models() -> Dict[str, Any]:
    """
    Get information about available Bayesian models.
    
    Returns:
        Dictionary containing model information
    """
    models_info = {}
    
    for model_name, schema in MODEL_SCHEMAS.items(): # type: ignore
        models_info[model_name] = {
            "description": schema["description"],
            "required_fields": schema["required_fields"],
            "optional_fields": schema["optional_fields"],
            "field_descriptions": schema["field_descriptions"]
        }
    
    return {
        "status": "success",
        "available_models": models_info,
        "total_models": len(MODEL_SCHEMAS)
    }


def validate_model_data(model: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate data against a specific model's schema.
    
    Args:
        model: Name of the Bayesian model
        data: Data to validate
    
    Returns:
        Dictionary containing validation results
    """
    if model not in MODEL_SCHEMAS:
        return {
            "is_valid": False,
            "error": f"Unknown model '{model}'",
            "available_models": list(MODEL_SCHEMAS.keys())
        }
    
    schema = MODEL_SCHEMAS[model]
    validation_result: Dict[str, Any] = {
        "is_valid": True,
        "model": model,
        "errors": [],
        "warnings": [],
        "missing_required": [],
        "invalid_types": [],
        "unknown_fields": []
    }
    
    # Check for missing required fields
    for field in schema["required_fields"]:
        if field not in data:
            validation_result["missing_required"].append(field)
            validation_result["is_valid"] = False
    
    # Check data types
    for field, value in data.items():
        if field in schema["field_types"]:
            expected_type = schema["field_types"][field]
            if not isinstance(value, expected_type):
                validation_result["invalid_types"].append({
                    "field": field,
                    "expected": expected_type.__name__,
                    "actual": type(value).__name__
                })
                validation_result["is_valid"] = False
        elif field not in schema["optional_fields"]:
            validation_result["unknown_fields"].append(field)
            validation_result["warnings"].append(f"Unknown field '{field}' for model '{model}'")
    
    return validation_result


def batch_predict_sepsis(patient_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Perform batch sepsis predictions for multiple patients.
    
    Args:
        patient_data: List of dictionaries containing patient data
    
    Returns:
        Dictionary containing batch prediction results
    """
    if not patient_data:
        return {
            "error": "No patient data provided",
            "status": "error"
        }
    
    results: Dict[str, Any] = {
        "status": "success",
        "total_patients": len(patient_data),
        "successful_predictions": 0,
        "failed_predictions": 0,
        "results": []
    }
    
    for i, patient in enumerate(patient_data):
        try:
            # Extract required fields
            temp = patient.get("temp")
            hr = patient.get("hr")
            wbc = patient.get("wbc")
            
            # Check for missing required fields
            if temp is None or hr is None or wbc is None:
                result = {
                    "error": "Missing required fields: temp, hr, and wbc are required for sepsis prediction.",
                    "status": "error"
                }
            else:
                # Extract optional fields
                systolic_bp = patient.get("systolic_bp")
                diastolic_bp = patient.get("diastolic_bp")
                respiratory_rate = patient.get("respiratory_rate")
                
                # Make prediction
                result = predict_sepsis(temp, hr, wbc, systolic_bp, diastolic_bp, respiratory_rate)
            
            results["results"].append({
                "patient_index": i,
                "patient_data": patient,
                "prediction": result
            })
            
            if result.get("status") == "success":
                results["successful_predictions"] += 1
            else:
                results["failed_predictions"] += 1
                
        except Exception as e:
            results["results"].append({
                "patient_index": i,
                "patient_data": patient,
                "error": str(e)
            })
            results["failed_predictions"] += 1
    
    return results


def get_model_schema(model: str) -> Dict[str, Any]:
    """
    Get the schema for a specific model.
    
    Args:
        model: Name of the Bayesian model
    
    Returns:
        Dictionary containing model schema information
    """
    if model not in MODEL_SCHEMAS:
        return {
            "error": f"Unknown model '{model}'",
            "available_models": list(MODEL_SCHEMAS.keys()),
            "status": "error"
        }
    
    schema = MODEL_SCHEMAS[model]
    return {
        "status": "success",
        "model": model,
        "schema": {
            "description": schema["description"],
            "required_fields": schema["required_fields"],
            "optional_fields": schema["optional_fields"],
            "field_descriptions": schema["field_descriptions"],
            "field_types": {k: v.__name__ for k, v in schema["field_types"].items()}
        }
    }


# Export functions for use in other modules
__all__ = [
    "call_bayesian_model",
    "predict_sepsis",
    "get_available_models",
    "validate_model_data",
    "batch_predict_sepsis",
    "get_model_schema"
]
