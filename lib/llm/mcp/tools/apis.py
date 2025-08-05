"""
API service tools for MCP server - Medline, ClinicalTrials, and NCBI integration.
"""
from typing import Any, Dict, List, Optional, Union

from amt_nano.services.apis import NCBI, ClinicalTrials, ICD10Code, Medline
from typing_extensions import TypedDict

from settings import logger


def fetch_medline_info(icd10_code: str) -> Dict[str, Any]:
    """
    Fetch medical information from Medline using an ICD-10 code.
    
    Args:
        icd10_code: ICD-10 code (e.g., "E11.9", "J45.40")
    
    Returns:
        Dictionary containing medical information from Medline
    """    
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


class ClinicalTrial(TypedDict):
    nct_id: str
    title: str
    condition: str
    status: str
    phase: str
    enrollment: str
    location: List[Dict[str, Any]]
    sponsor: str
    start_date: str
    completion_date: str

class ClinicalTrialsResult(TypedDict):
    trials: List[ClinicalTrial]
    total_count: int
    condition: str
    source: str

class ClinicalTrialsError(TypedDict):
    error: str
    condition: str
    source: str


def fetch_clinical_trials(condition: str, max_results: int = 10) -> Union[ClinicalTrialsResult, ClinicalTrialsError]:
    """
    Fetch clinical trial data from ClinicalTrials.gov.
    
    Args:
        condition: Medical condition or disease to search for
        max_results: Maximum number of trials to return (default: 10)
    
    Returns:
        Dictionary containing clinical trial data
    """
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
        formatted_trials: List[ClinicalTrial] = []
        
        for trial in trials[:max_results]:
            formatted_trial: ClinicalTrial = {
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
        
        return ClinicalTrialsResult(
            trials=formatted_trials,
            total_count=len(trials),
            condition=condition,
            source="ClinicalTrials.gov"
        )
        
    except Exception as e:
        logger.error(f"Error in clinical trials fetch: {e}")
        return {
            "error": f"Failed to fetch clinical trials: {str(e)}",
            "condition": condition,
            "source": "ClinicalTrials.gov"
        }


class PubMedArticle(TypedDict):
    pmid: str
    title: str
    journal: str
    authors: str
    pubdate: str
    abstract: Optional[str]

class PubMedSearchResult(TypedDict):
    articles: List[PubMedArticle]
    total_count: int
    query: str
    source: str

class PubMedSearchError(TypedDict):
    error: str
    query: str
    source: str



def fetch_pubmed_studies(query: str, max_results: int = 10, include_abstracts: bool = False) -> Union[PubMedSearchResult, PubMedSearchError]:
    """
    Fetch medical studies and articles from NCBI's PubMed database.
    
    Args:
        query: Search query for PubMed articles
        max_results: Maximum number of articles to return (default: 10)
        include_abstracts: Whether to include article abstracts (default: False)
    
    Returns:
        Dictionary containing PubMed article data
    """
    try:
        # TODO: Pass these in via headers from frontend...
        ncbi_service = NCBI(
            email="user@example.com",
            logger=logger,
            api_key="your_api_key_here"
        )

        raise NotImplementedError("NCBI service is not implemented yet")  # Placeholder for actual NCBI service implementation
        
        # Fetch studies
        articles = ncbi_service.fetch_ncbi_studies(query, debug=False)
        
        # Format the results
        formatted_articles: List[PubMedArticle] = []
        for article in articles[:max_results]:
            formatted_article: PubMedArticle = {
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


class MedicalLiteratureSearchResult(TypedDict):
    condition: str
    sources: Dict[str, Any]
    summary: Dict[str, int]


def search_medical_literature(condition: str, max_results: int = 10) -> MedicalLiteratureSearchResult:
    """
    Comprehensive search across multiple medical literature sources.
    
    Args:
        condition: Medical condition or disease to search for
        max_results: Maximum number of results per source (default: 10)
    
    Returns:
        Dictionary containing results from multiple sources
    """
    results: MedicalLiteratureSearchResult = {
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
    if "error" not in trials_result and "trials" in trials_result:
        results["summary"]["total_trials"] = len(trials_result["trials"])
    
    # Fetch from PubMed
    pubmed_result = fetch_pubmed_studies(condition, max_results)
    results["sources"]["pubmed"] = pubmed_result
    if "error" not in pubmed_result and "articles" in pubmed_result:
        results["summary"]["total_articles"] = len(pubmed_result["articles"])
    
    # Count successful sources
    successful_sources = 0
    for source_data in results["sources"].values():
        if isinstance(source_data, dict) and "error" not in source_data:
            successful_sources += 1
    
    results["summary"]["total_sources"] = successful_sources
    
    return results


class Evidence(TypedDict):
    icd10_code: str
    condition: str
    medline_info: Dict[str, Any]
    literature: MedicalLiteratureSearchResult
    summary: Dict[str, bool]

def get_medical_evidence(icd10_code: str, condition: str) -> Evidence:
    """
    Get comprehensive medical evidence for a condition including Medline info and literature.
    
    Args:
        icd10_code: ICD-10 code for the condition
        condition: Human-readable condition name
    
    Returns:
        Dictionary containing comprehensive medical evidence
    """
    evidence: Evidence = {
        "icd10_code": icd10_code,
        "condition": condition,
        "medline_info": {},
        "literature": {
            "condition": condition,
            "sources": {},
            "summary": {
                "total_trials": 0,
                "total_articles": 0,
                "total_sources": 0
            }
        },
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
