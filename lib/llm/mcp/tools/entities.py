"""
ICD Autocoder tools for MCP server.
"""
from typing import Any, Dict, List, Union

from amt_nano.services.icd_autocoder_service import ICDAutoCoderService

from settings import logger


def predict_icd_codes(note_text: str, top_k: int = 5) -> Union[List[Dict[str, Any]], str]:
    """
    Map clinical free-text to ICD-10 codes using the ICD Autocoder service.
    
    Args:
        note_text: Clinical note or summary text
        top_k: Number of code candidates to return (default: 5, max: 10)
    
    Returns:
        List of dictionaries containing ICD codes and entity information
    """
    if not ICDAutoCoderService:
        logger.error("ICD Autocoder service not available, returning placeholder codes")
        return "ICD Autocoder service not available"
    try:
        # Initialize the ICD Autocoder service
        service: ICDAutoCoderService = ICDAutoCoderService(note_text)
        
        # Run the main processing pipeline
        result = service.main()
        
        # Extract ICD codes from the result
        icd_entities = result.get("icd_codes", [])
        
        # Format the results
        formatted_results: List[Dict[str, Any]] = []
        for entity in icd_entities[:top_k]:
            if entity.get("icd10cm"):
                formatted_results.append({
                    "code": entity["icd10cm"],
                    "name": entity.get("icd10cm_name", ""),
                    "text": entity.get("text", ""),
                    "cui": entity.get("cui"),
                    "start_char": entity.get("start_char", 0),
                    "end_char": entity.get("end_char", 0),
                    "confidence": 0.9 if entity.get("cui") else 0.7  # Higher confidence if UMLS CUI is available
                })
        
        # If no ICD codes found, return some default codes
        if not formatted_results:
            logger.warning("No ICD codes found.")
            return "No ICD codes found."
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error in ICD code prediction: {e}")
        return f"Error in ICD code prediction: {e}"


def extract_medical_entities(note_text: str) -> List[Dict[str, Any]]:
    """
    Extract medical entities from clinical text using the ICD Autocoder service.
    
    Args:
        note_text: Clinical note or summary text
    
    Returns:
        List of dictionaries containing extracted medical entities with positions
    """
    if not ICDAutoCoderService:
        logger.warning("ICD Autocoder service not available, returning placeholder entities")
        return [
            {"text": "diabetes", "label": "DISEASE", "start_char": 0, "end_char": 8, "cui": None},
            {"text": "hypertension", "label": "DISEASE", "start_char": 10, "end_char": 22, "cui": None}
        ]
    
    try:
        # Initialize the ICD Autocoder service
        service = ICDAutoCoderService(note_text)
        
        # Run the main processing pipeline
        result = service.main()
        
        # Extract entities from the result
        entities = result.get("normalized_entities", [])
        
        # Format the results
        formatted_entities: List[Dict[str, Any]] = []
        for entity in entities:
            formatted_entities.append({
                "text": entity.get("text", ""),
                "label": entity.get("label", ""),
                "start_char": entity.get("start_char", 0),
                "end_char": entity.get("end_char", 0),
                "cui": entity.get("cui"),
                "icd10cm": entity.get("icd10cm"),
                "icd10cm_name": entity.get("icd10cm_name")
            })
        
        return formatted_entities
        
    except Exception as e:
        logger.error(f"Error in entity extraction: {e}")
        return []


def get_icd_code_details(icd_code: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific ICD-10 code.
    
    Args:
        icd_code: ICD-10 code (e.g., "E11.9")
    
    Returns:
        Dictionary containing ICD code details
    """
    # This is a placeholder implementation
    # In a real implementation, you would query a medical database or API
    icd_details = {
        "E11.9": {
            "code": "E11.9",
            "name": "Type 2 diabetes mellitus without complications",
            "category": "Endocrine, nutritional and metabolic diseases",
            "block": "Diabetes mellitus",
            "chapter": "Endocrine, nutritional and metabolic diseases"
        },
        "I10": {
            "code": "I10",
            "name": "Essential (primary) hypertension",
            "category": "Diseases of the circulatory system",
            "block": "Hypertensive diseases",
            "chapter": "Diseases of the circulatory system"
        },
        "R53.83": {
            "code": "R53.83",
            "name": "Other fatigue",
            "category": "Symptoms, signs and abnormal clinical and laboratory findings",
            "block": "General symptoms and signs",
            "chapter": "Symptoms, signs and abnormal clinical and laboratory findings"
        }
    }
    
    return icd_details.get(icd_code, {
        "code": icd_code,
        "name": "Unknown ICD code",
        "category": "Unknown",
        "block": "Unknown",
        "chapter": "Unknown"
    })


def validate_icd_code(icd_code: str) -> Dict[str, Any]:
    """
    Validate if an ICD-10 code is properly formatted and exists.
    
    Args:
        icd_code: ICD-10 code to validate
    
    Returns:
        Dictionary containing validation results
    """
    import re

    # Basic ICD-10 format validation
    icd_pattern = r'^[A-Z]\d{2}(\.\d{1,2})?$'
    is_valid_format = bool(re.match(icd_pattern, icd_code))
    
    # Get details if format is valid
    details = None
    if is_valid_format:
        details = get_icd_code_details(icd_code)
    
    return {
        "code": icd_code,
        "is_valid_format": is_valid_format,
        "is_known_code": details.get("name", "") != "Unknown ICD code" if details else False,
        "details": details
    }


# Export functions for use in other modules
__all__ = [
    "predict_icd_codes",
    "extract_medical_entities", 
    "get_icd_code_details",
    "validate_icd_code"
]
