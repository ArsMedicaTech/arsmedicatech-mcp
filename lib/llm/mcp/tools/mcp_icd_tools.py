"""
MCP tool registration for ICD Autocoder functions.
"""
from typing import Any, Dict, List, Optional

from fastmcp import Context
from mcp_init import mcp
from pydantic import Field

from .entities import (extract_medical_entities, get_icd_code_details,
                       predict_icd_codes, validate_icd_code)


@mcp.tool
async def predict_icd_codes_tool(
    note_text: str = Field(description="Clinical note or summary text"),
    top_k: int = Field(default=5, ge=1, le=10, description="Number of code candidates to return"),
    ctx: Optional[Context] = None
) -> List[Dict[str, Any]]:
    """
    Map clinical free-text to ICD-10 codes using the ICD Autocoder service.
    """
    return predict_icd_codes(note_text, top_k)


@mcp.tool
async def extract_medical_entities_tool(
    note_text: str = Field(description="Clinical note or summary text"),
    ctx: Optional[Context] = None
) -> List[Dict[str, Any]]:
    """
    Extract medical entities from clinical text using the ICD Autocoder service.
    """
    return extract_medical_entities(note_text)


@mcp.tool
async def get_icd_code_details_tool(
    icd_code: str = Field(description="ICD-10 code (e.g., 'E11.9')"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific ICD-10 code.
    """
    return get_icd_code_details(icd_code)


@mcp.tool
async def validate_icd_code_tool(
    icd_code: str = Field(description="ICD-10 code to validate"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Validate if an ICD-10 code is properly formatted and exists.
    """
    return validate_icd_code(icd_code) 