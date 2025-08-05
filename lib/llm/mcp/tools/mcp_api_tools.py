"""
MCP tool registration for API service functions.
"""
from typing import Any, Dict, Optional

from fastmcp import Context
from mcp_init import mcp
from pydantic import Field

from .apis import (
    fetch_medline_info,
    fetch_clinical_trials,
    fetch_pubmed_studies,
    search_medical_literature,
    get_medical_evidence,
    validate_icd10_code
)


@mcp.tool
async def fetch_medline_info_tool(
    icd10_code: str = Field(description="ICD-10 code (e.g., 'E11.9', 'J45.40')"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Fetch medical information from Medline using an ICD-10 code.
    """
    return fetch_medline_info(icd10_code)


@mcp.tool
async def fetch_clinical_trials_tool(
    condition: str = Field(description="Medical condition or disease to search for"),
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of trials to return"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Fetch clinical trial data from ClinicalTrials.gov.
    """
    return fetch_clinical_trials(condition, max_results)


@mcp.tool
async def fetch_pubmed_studies_tool(
    query: str = Field(description="Search query for PubMed articles"),
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of articles to return"),
    include_abstracts: bool = Field(default=False, description="Whether to include article abstracts"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Fetch medical studies and articles from NCBI's PubMed database.
    """
    return fetch_pubmed_studies(query, max_results, include_abstracts)


@mcp.tool
async def search_medical_literature_tool(
    condition: str = Field(description="Medical condition or disease to search for"),
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of results per source"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Comprehensive search across multiple medical literature sources.
    """
    return search_medical_literature(condition, max_results)


@mcp.tool
async def get_medical_evidence_tool(
    icd10_code: str = Field(description="ICD-10 code for the condition"),
    condition: str = Field(description="Human-readable condition name"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get comprehensive medical evidence for a condition including Medline info and literature.
    """
    return get_medical_evidence(icd10_code, condition)


@mcp.tool
async def validate_icd10_code_tool(
    icd10_code: str = Field(description="ICD-10 code to validate"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Validate an ICD-10 code format and check if it's supported.
    """
    return validate_icd10_code(icd10_code) 