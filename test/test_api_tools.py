#!/usr/bin/env python3
"""
Test script for API service tools.
"""
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib.llm.mcp.tools.apis import (fetch_clinical_trials, fetch_medline_info,
                                    fetch_pubmed_studies, get_medical_evidence,
                                    search_medical_literature,
                                    validate_icd10_code)


def test_api_tools():
    """Test the API service functions."""
    print("Testing API Service Tools")
    print("=" * 50)
    
    # Test data
    test_icd_code = "E11.9"
    test_condition = "diabetes"
    
    print(f"Test ICD-10 code: {test_icd_code}")
    print(f"Test condition: {test_condition}")
    print()
    
    # Test ICD-10 code validation
    print("1. Testing ICD-10 code validation:")
    validation = validate_icd10_code(test_icd_code)
    print(f"   {test_icd_code}: Valid={validation.get('is_valid', False)}")
    print()
    
    # Test Medline info fetch
    print("2. Testing Medline info fetch:")
    medline_info = fetch_medline_info(test_icd_code)
    if "error" not in medline_info:
        print(f"   Condition: {medline_info.get('condition', 'N/A')}")
        print(f"   Description: {medline_info.get('description', 'N/A')}")
        print(f"   Source: {medline_info.get('source', 'N/A')}")
    else:
        print(f"   Error: {medline_info.get('error', 'Unknown error')}")
    print()
    
    # Test clinical trials fetch
    print("3. Testing clinical trials fetch:")
    trials = fetch_clinical_trials(test_condition, max_results=3)
    if "trials" in trials:
        print(f"   Found {len(trials['trials'])} trials")
        for i, trial in enumerate(trials['trials'][:2], 1):
            print(f"   {i}. {trial.get('title', 'N/A')} ({trial.get('status', 'N/A')})")
    else:
        print(f"   Error: {trials.get('error', 'Unknown error')}")
    print()
    
    # Test PubMed studies fetch
    print("4. Testing PubMed studies fetch:")
    pubmed_studies = fetch_pubmed_studies(test_condition, max_results=3)
    if "articles" in pubmed_studies:
        print(f"   Found {len(pubmed_studies['articles'])} articles")
        for i, article in enumerate(pubmed_studies['articles'][:2], 1):
            print(f"   {i}. {article.get('title', 'N/A')} ({article.get('journal', 'N/A')})")
    else:
        print(f"   Error: {pubmed_studies.get('error', 'Unknown error')}")
    print()
    
    # Test comprehensive literature search
    print("5. Testing comprehensive literature search:")
    literature = search_medical_literature(test_condition, max_results=5)
    summary = literature.get('summary', {})
    print(f"   Total trials: {summary.get('total_trials', 0)}")
    print(f"   Total articles: {summary.get('total_articles', 0)}")
    print(f"   Total sources: {summary.get('total_sources', 0)}")
    print()
    
    # Test comprehensive medical evidence
    print("6. Testing comprehensive medical evidence:")
    evidence = get_medical_evidence(test_icd_code, test_condition)
    evidence_summary = evidence.get('summary', {})
    print(f"   Has Medline data: {evidence_summary.get('has_medline_data', False)}")
    print(f"   Has literature data: {evidence_summary.get('has_literature_data', False)}")
    print()
    
    print("All tests completed!")


if __name__ == "__main__":
    test_api_tools() 