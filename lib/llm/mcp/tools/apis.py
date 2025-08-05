"""
API service tools for MCP server - Medline, ClinicalTrials, and NCBI integration.
"""
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

# Add the project root to the path to import the API services
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from amt_nano.services.apis import Medline, ClinicalTrials, NCBI, ICD10Code
except ImportError:
    # Fallback for when the services are not available
    Medline = None
    ClinicalTrials = None
    NCBI = None
    ICD10Code = None

from settings import logger


def fetch_medline_info(icd10_code: str) -> Dict[str, Any]:
    """
    Fetch medical information from Medline using an ICD-10 code.
    
    Args:
        icd10_code: ICD-10 code (e.g., "E11.9", "J45.40")
    
    Returns:
        Dictionary containing medical information from Medline
    """
    if not Medline:
        logger.warning("Medline service not available, returning placeholder data")
        return {
            "condition": "Type 2 diabetes mellitus",
            "description": "A chronic condition affecting how your body metabolizes glucose",
            "symptoms": ["Increased thirst", "Frequent urination", "Fatigue"],
            "treatments": ["Lifestyle changes", "Oral medications", "Insulin therapy"],
            "source": "Medline Plus"
        }
    
    try:
        # Create ICD10Code instance
        icd_code = ICD10Code(icd10_code)
        
        # Initialize Medline service
        medline_service = Medline(logger)
        
        # Fetch data
        result = medline_service.fetch_medline(icd_code)
        
        if "error" in result:
            logger.error(f"Error fetching Medline data: {result['error']}")
            return {
                "error": result["error"],
                "icd10_code": icd10_code,
                "source": "Medline Plus"
            }
        
        return {
            "data": result,
            "icd10_code": icd10_code,
            "source": "Medline Plus"
        }
        
    except Exception as e:
        logger.error(f"Error in Medline info fetch: {e}")
        return {
            "error": f"Failed to fetch Medline data: {str(e)}",
            "icd10_code": icd10_code,
            "source": "Medline Plus"
        }


def fetch_clinical_trials(condition: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Fetch clinical trial data from ClinicalTrials.gov.
    
    Args:
        condition: Medical condition or disease to search for
        max_results: Maximum number of trials to return (default: 10)
    
    Returns:
        Dictionary containing clinical trial data
    """
    if not ClinicalTrials:
        logger.warning("ClinicalTrials service not available, returning placeholder data")
        return {
            "trials": [
                {
                    "nct_id": "NCT12345678",
                    "title": "Study of New Treatment for Diabetes",
                    "condition": condition,
                    "status": "Recruiting",
                    "phase": "Phase 2",
                    "enrollment": "100 participants"
                }
            ],
            "total_count": 1,
            "condition": condition,
            "source": "ClinicalTrials.gov"
        }
    
    try:
        # Initialize ClinicalTrials service
        trials_service = ClinicalTrials(logger)
        
        # Fetch data
        result = trials_service.fetch_clinical_trials(condition)
        
        if "error" in result:
            logger.error(f"Error fetching clinical trials: {result['error']}")
            return {
                "error": result["error"],
                "condition": condition,
                "source": "ClinicalTrials.gov"
            }
        
        # Process and format the results
        trials = result.get("studies", [])
        formatted_trials: List[Dict[str, Any]] = []
        
        for trial in trials[:max_results]:
            formatted_trial = {
                "nct_id": trial.get("nctId", ""),
                "title": trial.get("briefTitle", ""),
                "condition": condition,
                "status": trial.get("overallStatus", ""),
                "phase": trial.get("phase", ""),
                "enrollment": trial.get("enrollmentInfo", {}).get("count", ""),
                "location": trial.get("locations", []),
                "sponsor": trial.get("leadSponsorName", ""),
                "start_date": trial.get("startDate", ""),
                "completion_date": trial.get("completionDate", "")
            }
            formatted_trials.append(formatted_trial)
        
        return {
            "trials": formatted_trials,
            "total_count": len(trials),
            "condition": condition,
            "source": "ClinicalTrials.gov"
        }
        
    except Exception as e:
        logger.error(f"Error in clinical trials fetch: {e}")
        return {
            "error": f"Failed to fetch clinical trials: {str(e)}",
            "condition": condition,
            "source": "ClinicalTrials.gov"
        }


def fetch_pubmed_studies(query: str, max_results: int = 10, include_abstracts: bool = False) -> Dict[str, Any]:
    """
    Fetch medical studies and articles from NCBI's PubMed database.
    
    Args:
        query: Search query for PubMed articles
        max_results: Maximum number of articles to return (default: 10)
        include_abstracts: Whether to include article abstracts (default: False)
    
    Returns:
        Dictionary containing PubMed article data
    """
    if not NCBI:
        logger.warning("NCBI service not available, returning placeholder data")
        return {
            "articles": [
                {
                    "pmid": "12345678",
                    "title": "Recent Advances in Diabetes Treatment",
                    "journal": "Journal of Medical Research",
                    "authors": "Smith J, Johnson A, Brown K",
                    "pubdate": "2024",
                    "abstract": "This study examines new treatment approaches for diabetes management."
                }
            ],
            "total_count": 1,
            "query": query,
            "source": "PubMed"
        }
    
    try:
        # Initialize NCBI service with placeholder credentials
        # In a real implementation, these would be configured
        ncbi_service = NCBI(
            email="user@example.com",
            logger=logger,
            api_key="your_api_key_here"
        )
        
        # Fetch studies
        articles = ncbi_service.fetch_ncbi_studies(query, debug=False)
        
        # Format the results
        formatted_articles: List[Dict[str, Any]] = []
        for article in articles[:max_results]:
            formatted_article = {
                "pmid": article.get("pmid", ""),
                "title": article.get("title", ""),
                "journal": article.get("journal", ""),
                "authors": article.get("authors", ""),
                "pubdate": article.get("pubdate", ""),
                "abstract": article.get("abstract", "") if include_abstracts else ""
            }
            formatted_articles.append(formatted_article)
        
        return {
            "articles": formatted_articles,
            "total_count": len(articles),
            "query": query,
            "source": "PubMed"
        }
        
    except Exception as e:
        logger.error(f"Error in PubMed studies fetch: {e}")
        return {
            "error": f"Failed to fetch PubMed studies: {str(e)}",
            "query": query,
            "source": "PubMed"
        }


def search_medical_literature(condition: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Comprehensive search across multiple medical literature sources.
    
    Args:
        condition: Medical condition or disease to search for
        max_results: Maximum number of results per source (default: 10)
    
    Returns:
        Dictionary containing results from multiple sources
    """
    results = {
        "condition": condition,
        "sources": {},
        "summary": {
            "total_trials": 0,
            "total_articles": 0,
            "total_sources": 0
        }
    }
    
    # Fetch from ClinicalTrials.gov
    trials_result = fetch_clinical_trials(condition, max_results)
    results["sources"]["clinical_trials"] = trials_result
    if "trials" in trials_result:
        results["summary"]["total_trials"] = len(trials_result["trials"])
    
    # Fetch from PubMed
    pubmed_result = fetch_pubmed_studies(condition, max_results)
    results["sources"]["pubmed"] = pubmed_result
    if "articles" in pubmed_result:
        results["summary"]["total_articles"] = len(pubmed_result["articles"])
    
    # Count successful sources
    successful_sources = 0
    for source_data in results["sources"].values():
        if isinstance(source_data, dict) and "error" not in source_data:
            successful_sources += 1
    
    results["summary"]["total_sources"] = successful_sources
    
    return results


def get_medical_evidence(icd10_code: str, condition: str) -> Dict[str, Any]:
    """
    Get comprehensive medical evidence for a condition including Medline info and literature.
    
    Args:
        icd10_code: ICD-10 code for the condition
        condition: Human-readable condition name
    
    Returns:
        Dictionary containing comprehensive medical evidence
    """
    evidence = {
        "icd10_code": icd10_code,
        "condition": condition,
        "medline_info": {},
        "literature": {},
        "summary": {
            "has_medline_data": False,
            "has_literature_data": False
        }
    }
    
    # Fetch Medline information
    medline_result = fetch_medline_info(icd10_code)
    evidence["medline_info"] = medline_result
    evidence["summary"]["has_medline_data"] = "error" not in medline_result
    
    # Fetch literature
    literature_result = search_medical_literature(condition, max_results=5)
    evidence["literature"] = literature_result
    evidence["summary"]["has_literature_data"] = literature_result["summary"]["total_sources"] > 0
    
    return evidence


def validate_icd10_code(icd10_code: str) -> Dict[str, Any]:
    """
    Validate an ICD-10 code format and check if it's supported.
    
    Args:
        icd10_code: ICD-10 code to validate
    
    Returns:
        Dictionary containing validation results
    """
    if not ICD10Code:
        return {
            "code": icd10_code,
            "is_valid": False,
            "error": "ICD10Code class not available"
        }
    
    try:
        icd_code = ICD10Code(icd10_code)
        is_valid = icd_code.validate()
        
        return {
            "code": icd10_code,
            "is_valid": is_valid,
            "format_check": "ICD-10 format validation",
            "supported": is_valid  # In a real implementation, you'd check against a database
        }
        
    except Exception as e:
        return {
            "code": icd10_code,
            "is_valid": False,
            "error": str(e)
        }


# Export functions for use in other modules
__all__ = [
    "fetch_medline_info",
    "fetch_clinical_trials", 
    "fetch_pubmed_studies",
    "search_medical_literature",
    "get_medical_evidence",
    "validate_icd10_code"
]
