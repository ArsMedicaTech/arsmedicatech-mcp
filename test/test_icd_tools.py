#!/usr/bin/env python3
"""
Test script for ICD Autocoder tools.
"""
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib.llm.mcp.tools.entities import (
    predict_icd_codes,
    extract_medical_entities,
    get_icd_code_details,
    validate_icd_code
)


def test_icd_tools():
    """Test the ICD Autocoder functions."""
    print("Testing ICD Autocoder Tools")
    print("=" * 50)
    
    # Test data
    test_note = "Patient presents with Type 2 diabetes mellitus and essential hypertension. Also complains of fatigue and malaise."
    
    print(f"Test note: {test_note}")
    print()
    
    # Test ICD code prediction
    print("1. Testing ICD code prediction:")
    icd_codes = predict_icd_codes(test_note, top_k=3)
    for i, code in enumerate(icd_codes, 1):
        print(f"   {i}. {code}")
    print()
    
    # Test entity extraction
    print("2. Testing medical entity extraction:")
    entities = extract_medical_entities(test_note)
    for i, entity in enumerate(entities, 1):
        print(f"   {i}. {entity}")
    print()
    
    # Test ICD code details
    print("3. Testing ICD code details:")
    test_codes = ["E11.9", "I10", "R53.83", "INVALID"]
    for code in test_codes:
        details = get_icd_code_details(code)
        print(f"   {code}: {details['name']}")
    print()
    
    # Test ICD code validation
    print("4. Testing ICD code validation:")
    for code in test_codes:
        validation = validate_icd_code(code)
        print(f"   {code}: Valid format={validation['is_valid_format']}, Known={validation['is_known_code']}")
    print()
    
    print("All tests completed!")


if __name__ == "__main__":
    test_icd_tools() 