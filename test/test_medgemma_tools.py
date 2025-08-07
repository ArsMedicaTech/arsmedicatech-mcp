#!/usr/bin/env python3
"""
Test script for MedGemma medical vision tools.
"""
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib.llm.mcp.tools.medgemma import (
    analyze_medical_image,
    batch_analyze_medical_images,
    validate_medical_image_url,
)


def test_medgemma_tools():
    """Test the MedGemma medical vision functions."""
    print("Testing MedGemma Medical Vision Tools")
    print("=" * 50)

    # Test URLs (these are placeholder URLs for testing)
    test_urls = [
        "https://example.com/chest_xray.jpg",
        "https://example.com/dermatology_lesion.png",
        "https://example.com/pathology_slide.tiff",
        "https://example.com/mri_scan.jpg",
    ]

    # Test 1: URL validation
    print("1. Testing URL validation:")
    for url in test_urls:
        validation = validate_medical_image_url(url)
        print(f"   {url}: Valid={validation.get('is_valid', False)}")
        if validation.get("errors"):
            print(f"     Errors: {validation['errors']}")
        if validation.get("warnings"):
            print(f"     Warnings: {validation['warnings']}")
    print()

    # Test 2: Single image analysis
    print("2. Testing single image analysis:")
    test_image = "https://example.com/chest_xray.jpg"
    result = analyze_medical_image(
        test_image, view="PA", prompt="Describe any abnormalities"
    )
    print(f"   Image: {test_image}")
    print(f"   Status: {result.get('status', 'N/A')}")
    if result.get("status") == "success":
        findings = result.get("findings", {})
        print(f"   Image type: {findings.get('image_type', 'N/A')}")
        print(f"   Impression: {findings.get('impression', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
    else:
        print(f"   Error: {result.get('error', 'N/A')}")
    print()

    # Test 3: Dermatology image analysis
    print("3. Testing dermatology image analysis:")
    derm_image = "https://example.com/dermatology_lesion.png"
    derm_result = analyze_medical_image(
        derm_image, view="DermCloseUp", prompt="Assess the lesion"
    )
    print(f"   Image: {derm_image}")
    print(f"   Status: {derm_result.get('status', 'N/A')}")
    if derm_result.get("status") == "success":
        findings = derm_result.get("findings", {})
        print(f"   Image type: {findings.get('image_type', 'N/A')}")
        print(f"   Impression: {findings.get('impression', 'N/A')}")
        if "findings" in findings:
            lesion_findings = findings["findings"]
            if "lesion" in lesion_findings:
                print(
                    f"   Lesion status: {lesion_findings['lesion'].get('status', 'N/A')}"
                )
    print()

    # Test 4: Pathology image analysis
    print("4. Testing pathology image analysis:")
    path_image = "https://example.com/pathology_slide.tiff"
    path_result = analyze_medical_image(
        path_image, view="Other", prompt="Analyze cellular patterns"
    )
    print(f"   Image: {path_image}")
    print(f"   Status: {path_result.get('status', 'N/A')}")
    if path_result.get("status") == "success":
        findings = path_result.get("findings", {})
        print(f"   Image type: {findings.get('image_type', 'N/A')}")
        print(f"   Impression: {findings.get('impression', 'N/A')}")
    print()

    # Test 5: Batch analysis
    print("5. Testing batch image analysis:")
    batch_result = batch_analyze_medical_images(test_urls[:3], view="PA")
    print(f"   Total images: {batch_result.get('total_images', 0)}")
    print(f"   Processed: {batch_result.get('processed_images', 0)}")
    print(f"   Failed: {batch_result.get('failed_images', 0)}")
    print()

    # Test 6: Error handling
    print("6. Testing error handling:")
    invalid_url = "invalid_url"
    error_result = analyze_medical_image(invalid_url)
    print(f"   Invalid URL: {invalid_url}")
    print(f"   Status: {error_result.get('status', 'N/A')}")
    print(f"   Error: {error_result.get('error', 'N/A')}")
    print()

    print("All tests completed!")


if __name__ == "__main__":
    test_medgemma_tools()
