"""
MCP tool registration for MedGemma medical vision functions.
"""

from typing import Any, Dict, List, Optional

from fastmcp import Context
from pydantic import Field

from .mcp_icd_tools import mcp  # type: ignore
from .medgemma import (
    analyze_medical_image,
    batch_analyze_medical_images,
    validate_medical_image_url,
)


@mcp.tool
async def analyze_medical_image_tool(
    image_url: str = Field(
        description="Public or signed URL to a PNG/JPG X-ray, derm photo, pathology slide, etc."
    ),
    view: Optional[str] = Field(
        default=None,
        description="Optional imaging view / angle (AP, PA, Lateral, DermCloseUp, Other)",
    ),
    prompt: Optional[str] = Field(
        default=None,
        description="Optional free-text question for the model (e.g. 'Describe notable abnormalities')",
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Run MedGemma-4B vision-language model on a medical image and return structured findings.
    """
    return analyze_medical_image(image_url, view, prompt)


@mcp.tool
async def batch_analyze_medical_images_tool(
    image_urls: List[str] = Field(description="List of image URLs to analyze"),
    view: Optional[str] = Field(
        default=None, description="Optional imaging view / angle"
    ),
    prompt: Optional[str] = Field(
        default=None, description="Optional free-text question for the model"
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Analyze multiple medical images in batch.
    """
    return batch_analyze_medical_images(image_urls, view, prompt)


@mcp.tool
async def validate_medical_image_url_tool(
    image_url: str = Field(description="The image URL to validate"),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Validate a medical image URL for accessibility and format.
    """
    return validate_medical_image_url(image_url)
