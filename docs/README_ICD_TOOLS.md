# ICD Autocoder Tools

This module provides functions to interact with the ICD Autocoder service for extracting medical entities and predicting ICD-10 codes from clinical text.

## Functions

### `predict_icd_codes(note_text: str, top_k: int = 5) -> List[Dict[str, Any]]`

Maps clinical free-text to ICD-10 codes using the ICD Autocoder service.

**Parameters:**
- `note_text`: Clinical note or summary text
- `top_k`: Number of code candidates to return (default: 5, max: 10)

**Returns:**
- List of dictionaries containing ICD codes and entity information

**Example:**
```python
from lib.llm.mcp.tools.entities import predict_icd_codes

note = "Patient presents with Type 2 diabetes mellitus and essential hypertension."
codes = predict_icd_codes(note, top_k=3)
# Returns: [
#   {"code": "E11.9", "name": "Type 2 diabetes mellitus without complications", "text": "diabetes", "confidence": 0.9},
#   {"code": "I10", "name": "Essential (primary) hypertension", "text": "hypertension", "confidence": 0.9}
# ]
```

### `extract_medical_entities(note_text: str) -> List[Dict[str, Any]]`

Extracts medical entities from clinical text using the ICD Autocoder service.

**Parameters:**
- `note_text`: Clinical note or summary text

**Returns:**
- List of dictionaries containing extracted medical entities with positions

**Example:**
```python
from lib.llm.mcp.tools.entities import extract_medical_entities

note = "Patient presents with Type 2 diabetes mellitus and essential hypertension."
entities = extract_medical_entities(note)
# Returns: [
#   {"text": "Type 2 diabetes mellitus", "label": "DISEASE", "start_char": 22, "end_char": 46, "cui": "C0011849"},
#   {"text": "essential hypertension", "label": "DISEASE", "start_char": 51, "end_char": 73, "cui": "C0020538"}
# ]
```

### `get_icd_code_details(icd_code: str) -> Dict[str, Any]`

Gets detailed information about a specific ICD-10 code.

**Parameters:**
- `icd_code`: ICD-10 code (e.g., "E11.9")

**Returns:**
- Dictionary containing ICD code details

**Example:**
```python
from lib.llm.mcp.tools.entities import get_icd_code_details

details = get_icd_code_details("E11.9")
# Returns: {
#   "code": "E11.9",
#   "name": "Type 2 diabetes mellitus without complications",
#   "category": "Endocrine, nutritional and metabolic diseases",
#   "block": "Diabetes mellitus",
#   "chapter": "Endocrine, nutritional and metabolic diseases"
# }
```

### `validate_icd_code(icd_code: str) -> Dict[str, Any]`

Validates if an ICD-10 code is properly formatted and exists.

**Parameters:**
- `icd_code`: ICD-10 code to validate

**Returns:**
- Dictionary containing validation results

**Example:**
```python
from lib.llm.mcp.tools.entities import validate_icd_code

validation = validate_icd_code("E11.9")
# Returns: {
#   "code": "E11.9",
#   "is_valid_format": True,
#   "is_known_code": True,
#   "details": {...}
# }
```

## MCP Integration

The functions are also available as MCP tools when the MCP framework is available:

- `predict_icd_codes_tool`: MCP tool for ICD code prediction
- `extract_medical_entities_tool`: MCP tool for entity extraction
- `get_icd_code_details_tool`: MCP tool for ICD code details
- `validate_icd_code_tool`: MCP tool for ICD code validation

## Dependencies

The functions require the `amt_nano.services.icd_autocoder_service` module to be available. If the service is not available, the functions will return placeholder data.

## Testing

Run the test script to see the functions in action:

```bash
python test_icd_tools.py
```

## Error Handling

All functions include proper error handling and will return fallback data if the ICD Autocoder service is not available or encounters errors. The functions log warnings and errors using the configured logger.

## Integration with ICD Autocoder Service

The functions integrate with the ICD Autocoder service which:

1. **NER Extraction**: Uses an external NER API to extract named entities from clinical text
2. **UMLS Normalization**: Normalizes entities using the UMLS API to get CUIs (Concept Unique Identifiers)
3. **ICD Code Matching**: Matches normalized entities to ICD-10-CM codes
4. **Caching**: Implements caching to improve performance for repeated queries

The service processes clinical text through this pipeline and returns structured data with ICD codes, entity positions, and confidence scores. 