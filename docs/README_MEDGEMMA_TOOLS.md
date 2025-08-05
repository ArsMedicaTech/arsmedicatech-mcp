# MedGemma Medical Vision Tools

This module provides tools for medical image analysis using the MedGemma-4B vision-language model, enabling automated analysis of various types of medical images including X-rays, dermatology photos, pathology slides, and other medical imaging modalities.

## Functions

### `analyze_medical_image(image_url: str, view: Optional[str] = None, prompt: Optional[str] = None) -> Dict[str, Any]`

Runs MedGemma-4B vision-language model on a medical image and returns structured findings.

**Parameters:**
- `image_url`: Public or signed URL to a PNG/JPG X-ray, derm photo, pathology slide, etc.
- `view`: Optional imaging view / angle (AP, PA, Lateral, DermCloseUp, Other)
- `prompt`: Optional free-text question for the model (e.g. 'Describe notable abnormalities')

**Returns:**
- Dictionary containing structured medical findings from the image analysis

**Example:**
```python
from lib.llm.mcp.tools.medgemma import analyze_medical_image

result = analyze_medical_image(
    "https://example.com/chest_xray.jpg",
    view="PA",
    prompt="Describe any abnormalities"
)
# Returns: {
#   "status": "success",
#   "image_url": "https://example.com/chest_xray.jpg",
#   "view": "PA",
#   "findings": {
#     "image_type": "Chest X-ray",
#     "findings": {
#       "lungs": {"status": "normal", "description": "Lungs appear clear..."},
#       "heart": {"status": "normal", "description": "Cardiac silhouette..."}
#     },
#     "impression": "Normal chest X-ray",
#     "recommendations": ["No immediate action required"]
#   },
#   "model": "MedGemma-4B",
#   "confidence": 0.85
# }
```

### `batch_analyze_medical_images(image_urls: List[str], view: Optional[str] = None, prompt: Optional[str] = None) -> Dict[str, Any]`

Analyzes multiple medical images in batch.

**Parameters:**
- `image_urls`: List of image URLs to analyze
- `view`: Optional imaging view / angle
- `prompt`: Optional free-text question for the model

**Returns:**
- Dictionary containing batch analysis results

**Example:**
```python
from lib.llm.mcp.tools.medgemma import batch_analyze_medical_images

urls = [
    "https://example.com/xray1.jpg",
    "https://example.com/xray2.jpg",
    "https://example.com/derm1.png"
]

batch_result = batch_analyze_medical_images(urls, view="PA")
# Returns: {
#   "status": "success",
#   "total_images": 3,
#   "processed_images": 3,
#   "failed_images": 0,
#   "results": [...]
# }
```

### `validate_medical_image_url(image_url: str) -> Dict[str, Any]`

Validates a medical image URL for accessibility and format.

**Parameters:**
- `image_url`: The image URL to validate

**Returns:**
- Dictionary containing validation results

**Example:**
```python
from lib.llm.mcp.tools.medgemma import validate_medical_image_url

validation = validate_medical_image_url("https://example.com/image.jpg")
# Returns: {
#   "is_valid": True,
#   "errors": [],
#   "warnings": [],
#   "image_info": {
#     "content_type": "image/jpeg",
#     "content_length": "1024000",
#     "last_modified": "Wed, 21 Oct 2023 07:28:00 GMT"
#   }
# }
```

## MCP Integration

The functions are also available as MCP tools when the MCP framework is available:

- `analyze_medical_image_tool`: MCP tool for single image analysis
- `batch_analyze_medical_images_tool`: MCP tool for batch image analysis
- `validate_medical_image_url_tool`: MCP tool for URL validation

## Dependencies

The functions require the MedGemma service to be available. If the service is not available, the functions will return placeholder data with appropriate warnings.

## Testing

Run the test script to see the functions in action:

```bash
python test_medgemma_tools.py
```

## Error Handling

All functions include proper error handling and will return fallback data if the MedGemma service is not available or encounters errors. The functions log warnings and errors using the configured logger.

## Integration with MedGemma Service

The functions integrate with the MedGemma-4B vision-language model which provides:

1. **Medical Image Analysis**: Automated analysis of various medical imaging modalities
2. **Structured Findings**: Organized results with confidence scores
3. **Multi-modal Support**: X-rays, dermatology, pathology, MRI, CT scans
4. **Custom Prompts**: Ability to ask specific questions about images

## Supported Image Types

### 1. **Chest X-rays**
- AP (Anteroposterior) and PA (Posteroanterior) views
- Analysis of lungs, heart, bones, and mediastinum
- Detection of infiltrates, masses, fractures, and other abnormalities

### 2. **Dermatology Images**
- Close-up photography of skin lesions
- Analysis of pigmentation, borders, size, and texture
- Assessment of suspicious features (ABCD criteria)

### 3. **Pathology Slides**
- Microscopic analysis of tissue samples
- Cellular pattern recognition
- Staining pattern analysis
- Nuclear morphology assessment

### 4. **Other Medical Imaging**
- MRI scans
- CT scans
- Ultrasound images
- Endoscopy images

## View Parameters

The following view parameters are supported:

- **AP**: Anteroposterior view (front-to-back)
- **PA**: Posteroanterior view (back-to-front)
- **Lateral**: Side view
- **DermCloseUp**: Close-up dermatology photography
- **Other**: General medical imaging

## Structured Output Format

The analysis results include:

```json
{
  "status": "success",
  "image_url": "https://example.com/image.jpg",
  "view": "PA",
  "findings": {
    "image_type": "Chest X-ray",
    "findings": {
      "lungs": {
        "status": "normal",
        "description": "Lungs appear clear with no evidence of infiltrates",
        "confidence": 0.9
      },
      "heart": {
        "status": "normal", 
        "description": "Cardiac silhouette appears normal",
        "confidence": 0.85
      }
    },
    "impression": "Normal chest X-ray",
    "recommendations": ["No immediate action required"]
  },
  "model": "MedGemma-4B",
  "confidence": 0.85
}
```

## Configuration

For production use, you'll need to configure:

1. **MedGemma API Endpoint**: Service URL for the MedGemma model
2. **Authentication**: API keys or credentials for the service
3. **Timeout Settings**: Based on image size and complexity
4. **Rate Limiting**: Respect API usage limits

## Use Cases

These tools are particularly useful for:

- **Radiology**: Automated X-ray analysis and screening
- **Dermatology**: Skin lesion assessment and triage
- **Pathology**: Tissue sample analysis and preliminary review
- **Emergency Medicine**: Rapid image analysis for urgent cases
- **Telemedicine**: Remote image analysis and consultation
- **Medical Education**: Training and case study analysis
- **Research**: Large-scale medical image analysis

## Best Practices

1. **Image Quality**: Ensure images are high resolution and properly exposed
2. **URL Accessibility**: Use publicly accessible or properly signed URLs
3. **View Specification**: Provide appropriate view parameters for better analysis
4. **Prompt Engineering**: Use specific prompts for targeted analysis
5. **Error Handling**: Always check status and handle errors appropriately
6. **Validation**: Validate URLs before processing
7. **Batch Processing**: Use batch analysis for multiple images to improve efficiency

## Privacy and Security

- **Data Privacy**: Ensure image URLs don't contain sensitive patient information
- **Access Control**: Use signed URLs for private images
- **Audit Trail**: Log analysis requests for compliance
- **Data Retention**: Follow healthcare data retention policies

## Performance Considerations

- **Image Size**: Larger images may take longer to process
- **Batch Processing**: Process multiple images together when possible
- **Caching**: Cache results for repeated analysis of the same image
- **Async Processing**: Use asynchronous processing for large batches 