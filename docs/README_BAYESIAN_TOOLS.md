# Bayesian Tools

This module provides functions to interact with Bayesian inference models for medical predictions, particularly focused on sepsis prediction and other clinical outcomes.

## Functions

### `call_bayesian_model(model: str, data: Dict[str, Any]) -> Dict[str, Any]`

Generic function to call any Bayesian model with arbitrary data.

**Parameters:**
- `model`: Name of the Bayesian model to use
- `data`: Dictionary containing the model input data

**Returns:**
- Dictionary containing the Bayesian inference results

**Example:**
```python
from lib.llm.mcp.tools.bayesian import call_bayesian_model

# Call sepsis model
result = call_bayesian_model("sepsis", {
    "temp": 38.5,
    "hr": 95,
    "wbc": 12.5,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "respiratory_rate": 18
})
# Returns: {
#   "model": "sepsis",
#   "prediction": 0.23,
#   "confidence": 0.85,
#   "status": "success"
# }
```

### `predict_sepsis(temp: float, hr: int, wbc: float, systolic_bp: Optional[int] = None, diastolic_bp: Optional[int] = None, respiratory_rate: Optional[int] = None) -> Dict[str, Any]`

Predict sepsis probability using the Bayesian sepsis model.

**Parameters:**
- `temp`: Temperature in Celsius
- `hr`: Heart rate in beats per minute
- `wbc`: White blood cell count in K/μL
- `systolic_bp`: Optional systolic blood pressure in mmHg
- `diastolic_bp`: Optional diastolic blood pressure in mmHg
- `respiratory_rate`: Optional respiratory rate in breaths per minute

**Returns:**
- Dictionary containing sepsis prediction results

**Example:**
```python
from lib.llm.mcp.tools.bayesian import predict_sepsis

result = predict_sepsis(
    temp=38.5,
    hr=95,
    wbc=12.5,
    systolic_bp=120,
    diastolic_bp=80,
    respiratory_rate=18
)
# Returns: {
#   "model": "sepsis",
#   "prediction": 0.23,
#   "confidence": 0.85,
#   "risk_level": "low",
#   "recommendations": ["Monitor vital signs", "Consider antibiotics"],
#   "status": "success"
# }
```

### `get_available_models() -> Dict[str, Any]`

Get information about available Bayesian models.

**Returns:**
- Dictionary containing available models and their descriptions

**Example:**
```python
from lib.llm.mcp.tools.bayesian import get_available_models

models = get_available_models()
# Returns: {
#   "models": {
#     "sepsis": {
#       "description": "Sepsis prediction model",
#       "required_fields": ["temp", "hr", "wbc"],
#       "optional_fields": ["systolic_bp", "diastolic_bp", "respiratory_rate"]
#     }
#   },
#   "status": "success"
# }
```

### `validate_model_data(model: str, data: Dict[str, Any]) -> Dict[str, Any]`

Validate data against a specific model's schema.

**Parameters:**
- `model`: Name of the Bayesian model
- `data`: Data to validate

**Returns:**
- Dictionary containing validation results

**Example:**
```python
from lib.llm.mcp.tools.bayesian import validate_model_data

validation = validate_model_data("sepsis", {
    "temp": 38.5,
    "hr": 95,
    "wbc": 12.5
})
# Returns: {
#   "is_valid": True,
#   "missing_fields": [],
#   "type_errors": [],
#   "status": "success"
# }
```

### `batch_predict_sepsis(patient_data: List[Dict[str, Any]]) -> Dict[str, Any]`

Perform batch sepsis predictions for multiple patients.

**Parameters:**
- `patient_data`: List of dictionaries containing patient data

**Returns:**
- Dictionary containing batch prediction results

**Example:**
```python
from lib.llm.mcp.tools.bayesian import batch_predict_sepsis

patients = [
    {"temp": 38.5, "hr": 95, "wbc": 12.5},
    {"temp": 37.2, "hr": 88, "wbc": 8.2},
    {"temp": 39.1, "hr": 110, "wbc": 15.8}
]

results = batch_predict_sepsis(patients)
# Returns: {
#   "predictions": [
#     {"patient_id": 0, "prediction": 0.23, "risk_level": "low"},
#     {"patient_id": 1, "prediction": 0.08, "risk_level": "very_low"},
#     {"patient_id": 2, "prediction": 0.67, "risk_level": "high"}
#   ],
#   "summary": {
#     "total_patients": 3,
#     "high_risk_count": 1,
#     "average_prediction": 0.33
#   },
#   "status": "success"
# }
```

### `get_model_schema(model: str) -> Dict[str, Any]`

Get the schema for a specific model.

**Parameters:**
- `model`: Name of the Bayesian model

**Returns:**
- Dictionary containing the model schema

**Example:**
```python
from lib.llm.mcp.tools.bayesian import get_model_schema

schema = get_model_schema("sepsis")
# Returns: {
#   "model": "sepsis",
#   "description": "Sepsis prediction model",
#   "required_fields": ["temp", "hr", "wbc"],
#   "optional_fields": ["systolic_bp", "diastolic_bp", "respiratory_rate"],
#   "field_descriptions": {
#     "temp": "Temperature in Celsius",
#     "hr": "Heart rate in beats per minute",
#     "wbc": "White blood cell count in K/μL"
#   },
#   "field_types": {
#     "temp": "float",
#     "hr": "int",
#     "wbc": "float"
#   },
#   "status": "success"
# }
```

## Model Schemas

### Sepsis Model

The sepsis prediction model requires the following parameters:

**Required Fields:**
- `temp` (float): Temperature in Celsius
- `hr` (int): Heart rate in beats per minute  
- `wbc` (float): White blood cell count in K/μL

**Optional Fields:**
- `systolic_bp` (int): Systolic blood pressure in mmHg
- `diastolic_bp` (int): Diastolic blood pressure in mmHg
- `respiratory_rate` (int): Respiratory rate in breaths per minute

## Error Handling

All functions return a dictionary with a `status` field that can be:
- `"success"`: Operation completed successfully
- `"error"`: An error occurred (check the `error` field for details)

Common error scenarios:
- Invalid model name
- Missing required fields
- Invalid data types
- Network connectivity issues
- API service unavailable

## API Configuration

The Bayesian tools connect to the Bayesian inference service at:
- Production: `https://demo.arsmedicatech.com`
- Development: `http://localhost:62295`

## Usage Examples

### Basic Sepsis Prediction
```python
from lib.llm.mcp.tools.bayesian import predict_sepsis

# Simple prediction with required fields only
result = predict_sepsis(temp=38.5, hr=95, wbc=12.5)

# Full prediction with all fields
result = predict_sepsis(
    temp=38.5,
    hr=95, 
    wbc=12.5,
    systolic_bp=120,
    diastolic_bp=80,
    respiratory_rate=18
)
```

### Batch Processing
```python
from lib.llm.mcp.tools.bayesian import batch_predict_sepsis

# Process multiple patients
patients = [
    {"temp": 38.5, "hr": 95, "wbc": 12.5},
    {"temp": 37.2, "hr": 88, "wbc": 8.2},
    {"temp": 39.1, "hr": 110, "wbc": 15.8}
]

batch_results = batch_predict_sepsis(patients)
```

### Model Validation
```python
from lib.llm.mcp.tools.bayesian import validate_model_data, get_model_schema

# Check what models are available
schema = get_model_schema("sepsis")

# Validate data before prediction
validation = validate_model_data("sepsis", {
    "temp": 38.5,
    "hr": 95,
    "wbc": 12.5
})

if validation["is_valid"]:
    # Proceed with prediction
    result = predict_sepsis(temp=38.5, hr=95, wbc=12.5)
```

## Integration with MCP Server

These functions are registered as MCP tools and can be called through the MCP server interface. The tools are available as:

- `call_bayesian_model_tool`
- `predict_sepsis_tool`
- `get_available_models_tool`
- `validate_model_data_tool`
- `batch_predict_sepsis_tool`
- `get_model_schema_tool`

Each tool maintains the same function signature as the underlying Python functions but is adapted for MCP protocol communication. 