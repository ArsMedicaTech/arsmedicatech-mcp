"""
MCP tool registration for Bayesian API functions.
"""
from typing import Any, Dict, List, Optional

from fastmcp import Context
from mcp_init import mcp
from pydantic import Field

from .bayesian import (batch_predict_sepsis, call_bayesian_model,
                       get_available_models, get_model_schema, predict_sepsis,
                       validate_model_data)


@mcp.tool
async def call_bayesian_model_tool(
    model: str = Field(description="Name of the Bayesian model to use"),
    data: Dict[str, Any] = Field(description="Dictionary containing the model input data"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Generic function to call any Bayesian model with arbitrary data.
    """
    return call_bayesian_model(model, data)


@mcp.tool
async def predict_sepsis_tool(
    temp: float = Field(description="Temperature in Celsius"),
    hr: int = Field(description="Heart rate in beats per minute"),
    wbc: float = Field(description="White blood cell count in K/μL"),
    systolic_bp: Optional[int] = Field(default=None, description="Optional systolic blood pressure in mmHg"),
    diastolic_bp: Optional[int] = Field(default=None, description="Optional diastolic blood pressure in mmHg"),
    respiratory_rate: Optional[int] = Field(default=None, description="Optional respiratory rate in breaths per minute"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Predict sepsis probability using the Bayesian sepsis model.
    """
    return predict_sepsis(temp, hr, wbc, systolic_bp, diastolic_bp, respiratory_rate)


@mcp.tool
async def get_available_models_tool(
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get information about available Bayesian models.
    """
    return get_available_models()


@mcp.tool
async def validate_model_data_tool(
    model: str = Field(description="Name of the Bayesian model"),
    data: Dict[str, Any] = Field(description="Data to validate"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Validate data against a specific model's schema.
    """
    return validate_model_data(model, data)


@mcp.tool
async def batch_predict_sepsis_tool(
    patient_data: List[Dict[str, Any]] = Field(description="List of dictionaries containing patient data"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Perform batch sepsis predictions for multiple patients.
    """
    return batch_predict_sepsis(patient_data)


@mcp.tool
async def get_model_schema_tool(
    model: str = Field(description="Name of the Bayesian model"),
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Get the schema for a specific model.
    """
    return get_model_schema(model) 