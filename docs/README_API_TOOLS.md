# API Service Tools

This module provides functions to interact with various medical API services including Medline, ClinicalTrials.gov, and NCBI PubMed for comprehensive medical research and evidence gathering.

## Functions

### `fetch_medline_info(icd10_code: str) -> Dict[str, Any]`

Fetches medical information from Medline using an ICD-10 code.

**Parameters:**
- `icd10_code`: ICD-10 code (e.g., "E11.9", "J45.40")

**Returns:**
- Dictionary containing medical information from Medline

**Example:**
```python
from lib.llm.mcp.tools.apis import fetch_medline_info

info = fetch_medline_info("E11.9")
# Returns: {
#   "condition": "Type 2 diabetes mellitus",
#   "description": "A chronic condition affecting how your body metabolizes glucose",
#   "symptoms": ["Increased thirst", "Frequent urination", "Fatigue"],
#   "treatments": ["Lifestyle changes", "Oral medications", "Insulin therapy"],
#   "source": "Medline Plus"
# }
```

### `fetch_clinical_trials(condition: str, max_results: int = 10) -> Dict[str, Any]`

Fetches clinical trial data from ClinicalTrials.gov.

**Parameters:**
- `condition`: Medical condition or disease to search for
- `max_results`: Maximum number of trials to return (default: 10)

**Returns:**
- Dictionary containing clinical trial data

**Example:**
```python
from lib.llm.mcp.tools.apis import fetch_clinical_trials

trials = fetch_clinical_trials("diabetes", max_results=5)
# Returns: {
#   "trials": [
#     {
#       "nct_id": "NCT12345678",
#       "title": "Study of New Treatment for Diabetes",
#       "condition": "diabetes",
#       "status": "Recruiting",
#       "phase": "Phase 2",
#       "enrollment": "100 participants"
#     }
#   ],
#   "total_count": 1,
#   "condition": "diabetes",
#   "source": "ClinicalTrials.gov"
# }
```

### `fetch_pubmed_studies(query: str, max_results: int = 10, include_abstracts: bool = False) -> Dict[str, Any]`

Fetches medical studies and articles from NCBI's PubMed database.

**Parameters:**
- `query`: Search query for PubMed articles
- `max_results`: Maximum number of articles to return (default: 10)
- `include_abstracts`: Whether to include article abstracts (default: False)

**Returns:**
- Dictionary containing PubMed article data

**Example:**
```python
from lib.llm.mcp.tools.apis import fetch_pubmed_studies

articles = fetch_pubmed_studies("diabetes treatment", max_results=5, include_abstracts=True)
# Returns: {
#   "articles": [
#     {
#       "pmid": "12345678",
#       "title": "Recent Advances in Diabetes Treatment",
#       "journal": "Journal of Medical Research",
#       "authors": "Smith J, Johnson A, Brown K",
#       "pubdate": "2024",
#       "abstract": "This study examines new treatment approaches..."
#     }
#   ],
#   "total_count": 1,
#   "query": "diabetes treatment",
#   "source": "PubMed"
# }
```

### `search_medical_literature(condition: str, max_results: int = 10) -> Dict[str, Any]`

Comprehensive search across multiple medical literature sources.

**Parameters:**
- `condition`: Medical condition or disease to search for
- `max_results`: Maximum number of results per source (default: 10)

**Returns:**
- Dictionary containing results from multiple sources

**Example:**
```python
from lib.llm.mcp.tools.apis import search_medical_literature

literature = search_medical_literature("diabetes", max_results=5)
# Returns: {
#   "condition": "diabetes",
#   "sources": {
#     "clinical_trials": {...},
#     "pubmed": {...}
#   },
#   "summary": {
#     "total_trials": 5,
#     "total_articles": 10,
#     "total_sources": 2
#   }
# }
```

### `get_medical_evidence(icd10_code: str, condition: str) -> Dict[str, Any]`

Get comprehensive medical evidence for a condition including Medline info and literature.

**Parameters:**
- `icd10_code`: ICD-10 code for the condition
- `condition`: Human-readable condition name

**Returns:**
- Dictionary containing comprehensive medical evidence

**Example:**
```python
from lib.llm.mcp.tools.apis import get_medical_evidence

evidence = get_medical_evidence("E11.9", "diabetes")
# Returns: {
#   "icd10_code": "E11.9",
#   "condition": "diabetes",
#   "medline_info": {...},
#   "literature": {...},
#   "summary": {
#     "has_medline_data": True,
#     "has_literature_data": True
#   }
# }
```

### `validate_icd10_code(icd10_code: str) -> Dict[str, Any]`

Validates an ICD-10 code format and check if it's supported.

**Parameters:**
- `icd10_code`: ICD-10 code to validate

**Returns:**
- Dictionary containing validation results

**Example:**
```python
from lib.llm.mcp.tools.apis import validate_icd10_code

validation = validate_icd10_code("E11.9")
# Returns: {
#   "code": "E11.9",
#   "is_valid": True,
#   "format_check": "ICD-10 format validation",
#   "supported": True
# }
```

## MCP Integration

The functions are also available as MCP tools when the MCP framework is available:

- `fetch_medline_info_tool`: MCP tool for Medline information
- `fetch_clinical_trials_tool`: MCP tool for clinical trials
- `fetch_pubmed_studies_tool`: MCP tool for PubMed studies
- `search_medical_literature_tool`: MCP tool for comprehensive literature search
- `get_medical_evidence_tool`: MCP tool for comprehensive medical evidence
- `validate_icd10_code_tool`: MCP tool for ICD-10 code validation

## Dependencies

The functions require the `amt_nano.services.apis` module to be available. If the services are not available, the functions will return placeholder data.

## Testing

Run the test script to see the functions in action:

```bash
python test_api_tools.py
```

## Error Handling

All functions include proper error handling and will return fallback data if the API services are not available or encounter errors. The functions log warnings and errors using the configured logger.

## Integration with API Services

The functions integrate with three main medical API services:

### 1. **Medline Service**
- Fetches medical information using ICD-10 codes
- Provides condition descriptions, symptoms, and treatments
- Uses the Medline Plus API

### 2. **ClinicalTrials.gov Service**
- Searches for clinical trials by condition
- Returns trial details including status, phase, enrollment
- Uses the ClinicalTrials.gov API v2

### 3. **NCBI PubMed Service**
- Searches medical literature and studies
- Returns article metadata and optionally abstracts
- Uses the NCBI Entrez API with rate limiting

## Rate Limiting and Best Practices

- **PubMed API**: Implements automatic rate limiting (0.35s delay between requests)
- **ClinicalTrials.gov**: Respects API limits and provides structured data
- **Medline**: Uses public API with reasonable limits

## Configuration

For production use, you'll need to configure:

1. **NCBI API Key**: For PubMed access (optional but recommended)
2. **Email**: For NCBI API identification
3. **Rate Limiting**: Adjust delays based on your usage patterns

## Use Cases

These tools are particularly useful for:

- **Clinical Decision Support**: Gathering evidence for medical conditions
- **Research**: Finding relevant studies and trials
- **Medical Education**: Accessing up-to-date medical information
- **Drug Development**: Identifying ongoing clinical trials
- **Literature Reviews**: Comprehensive medical literature searches 