#!/usr/bin/env python3
"""
Test script for Bayesian tools.
"""
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib.llm.mcp.tools.bayesian import (batch_predict_sepsis,
                                        call_bayesian_model,
                                        get_available_models, get_model_schema,
                                        predict_sepsis, validate_model_data)


def test_bayesian_tools():
    """Test the Bayesian inference functions."""
    print("Testing Bayesian Tools")
    print("=" * 50)
    
    # Test data
    test_sepsis_data = {
        "temp": 38.5,
        "hr": 95,
        "wbc": 12.5,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "respiratory_rate": 18
    }
    
    test_patients = [
        {"temp": 38.5, "hr": 95, "wbc": 12.5},
        {"temp": 37.2, "hr": 88, "wbc": 8.2},
        {"temp": 39.1, "hr": 110, "wbc": 15.8}
    ]
    
    print(f"Test sepsis data: {test_sepsis_data}")
    print(f"Test patients count: {len(test_patients)}")
    print()
    
    # Test available models
    print("1. Testing available models:")
    models = get_available_models()
    if "models" in models:
        print(f"   Available models: {list(models['models'].keys())}")
        for model_name, model_info in models['models'].items():
            print(f"   - {model_name}: {model_info.get('description', 'N/A')}")
    else:
        print(f"   Error: {models.get('error', 'Unknown error')}")
    print()
    
    # Test model schema
    print("2. Testing model schema:")
    schema = get_model_schema("sepsis")
    if "model" in schema:
        print(f"   Model: {schema.get('model', 'N/A')}")
        print(f"   Description: {schema.get('description', 'N/A')}")
        print(f"   Required fields: {schema.get('required_fields', [])}")
        print(f"   Optional fields: {schema.get('optional_fields', [])}")
    else:
        print(f"   Error: {schema.get('error', 'Unknown error')}")
    print()
    
    # Test data validation
    print("3. Testing data validation:")
    validation = validate_model_data("sepsis", test_sepsis_data)
    if "is_valid" in validation:
        print(f"   Valid: {validation.get('is_valid', False)}")
        print(f"   Missing fields: {validation.get('missing_fields', [])}")
        print(f"   Type errors: {validation.get('type_errors', [])}")
    else:
        print(f"   Error: {validation.get('error', 'Unknown error')}")
    print()
    
    # Test sepsis prediction
    print("4. Testing sepsis prediction:")
    sepsis_result = predict_sepsis(
        temp=float(test_sepsis_data["temp"]),
        hr=int(test_sepsis_data["hr"]),
        wbc=float(test_sepsis_data["wbc"]),
        systolic_bp=int(test_sepsis_data["systolic_bp"]),
        diastolic_bp=int(test_sepsis_data["diastolic_bp"]),
        respiratory_rate=int(test_sepsis_data["respiratory_rate"])
    )
    if "prediction" in sepsis_result:
        print(f"   Prediction: {sepsis_result.get('prediction', 'N/A')}")
        print(f"   Confidence: {sepsis_result.get('confidence', 'N/A')}")
        print(f"   Risk level: {sepsis_result.get('risk_level', 'N/A')}")
        print(f"   Model: {sepsis_result.get('model', 'N/A')}")
    else:
        print(f"   Error: {sepsis_result.get('error', 'Unknown error')}")
    print()
    
    # Test generic model call
    print("5. Testing generic model call:")
    generic_result = call_bayesian_model("sepsis", test_sepsis_data)
    if "prediction" in generic_result:
        print(f"   Prediction: {generic_result.get('prediction', 'N/A')}")
        print(f"   Model: {generic_result.get('model', 'N/A')}")
        print(f"   Status: {generic_result.get('status', 'N/A')}")
    else:
        print(f"   Error: {generic_result.get('error', 'Unknown error')}")
    print()
    
    # Test batch prediction
    print("6. Testing batch prediction:")
    batch_result = batch_predict_sepsis(test_patients)
    if "predictions" in batch_result:
        predictions = batch_result.get('predictions', [])
        print(f"   Total predictions: {len(predictions)}")
        for i, pred in enumerate(predictions[:2], 1):
            print(f"   {i}. Patient {pred.get('patient_id', 'N/A')}: "
                  f"Prediction={pred.get('prediction', 'N/A')}, "
                  f"Risk={pred.get('risk_level', 'N/A')}")
        
        summary = batch_result.get('summary', {})
        print(f"   Summary - Total patients: {summary.get('total_patients', 0)}")
        print(f"   Summary - High risk count: {summary.get('high_risk_count', 0)}")
        print(f"   Summary - Average prediction: {summary.get('average_prediction', 0)}")
    else:
        print(f"   Error: {batch_result.get('error', 'Unknown error')}")
    print()
    
    # Test error handling
    print("7. Testing error handling:")
    
    # Test invalid model
    invalid_model_result = call_bayesian_model("invalid_model", {})
    if "error" in invalid_model_result:
        print(f"   Invalid model error: {invalid_model_result.get('error', 'N/A')}")
    
    # Test missing required fields
    incomplete_data = {"temp": 38.5}  # Missing hr and wbc
    incomplete_result = validate_model_data("sepsis", incomplete_data)
    if "missing_fields" in incomplete_result:
        print(f"   Missing fields: {incomplete_result.get('missing_fields', [])}")
    
    # Test invalid data types
    invalid_types_data = {"temp": "not_a_number", "hr": 95, "wbc": 12.5}
    invalid_types_result = validate_model_data("sepsis", invalid_types_data)
    if "type_errors" in invalid_types_result:
        print(f"   Type errors: {invalid_types_result.get('type_errors', [])}")
    print()
    
    print("All tests completed!")


if __name__ == "__main__":
    test_bayesian_tools() 