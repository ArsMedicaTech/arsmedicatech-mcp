"""
MCP tool registration for Optimal service functions.
"""

from typing import Any, Dict, List, Optional

from fastmcp import Context
from pydantic import Field

from .mcp_medgemma_tools import mcp  # type: ignore
from .optimal import (
    create_linear_optimization_problem,
    create_portfolio_optimization,
    create_resource_allocation_problem,
    create_supply_chain_optimization,
    solve_optimization_problem,
    validate_optimization_problem,
)


@mcp.tool
async def create_linear_optimization_problem_tool(
    objective_type: str = Field(
        description="Type of optimization ('minimize' or 'maximize')"
    ),
    variables: List[Dict[str, Any]] = Field(
        description="List of variable definitions with bounds"
    ),
    constraints: List[Dict[str, Any]] = Field(
        description="List of constraint definitions"
    ),
    parameters: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional parameters for the optimization"
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Create a linear optimization problem for the Optimal service.
    """
    return create_linear_optimization_problem(
        objective_type, variables, constraints, parameters
    )


@mcp.tool
async def solve_optimization_problem_tool(
    problem_schema: Dict[str, Any] = Field(
        description="The optimization problem schema"
    ),
    api_key: str = Field(description="API key for the Optimal service"),
    timeout: int = Field(
        default=30, ge=10, le=300, description="Request timeout in seconds"
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Solve an optimization problem using the Optimal service.
    """
    return solve_optimization_problem(problem_schema, api_key, timeout)


@mcp.tool
async def create_portfolio_optimization_tool(
    assets: List[str] = Field(description="List of asset names"),
    expected_returns: List[float] = Field(
        description="List of expected returns for each asset"
    ),
    covariance_matrix: List[List[float]] = Field(
        description="Covariance matrix for asset returns"
    ),
    target_return: Optional[float] = Field(
        default=None, description="Optional target return constraint"
    ),
    risk_free_rate: float = Field(default=0.02, description="Risk-free rate"),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Create a portfolio optimization problem (Markowitz model).
    """
    return create_portfolio_optimization(
        assets, expected_returns, covariance_matrix, target_return, risk_free_rate
    )


@mcp.tool
async def create_resource_allocation_problem_tool(
    resources: List[str] = Field(description="List of available resources"),
    tasks: List[str] = Field(description="List of tasks to be allocated"),
    resource_capacities: Dict[str, float] = Field(
        description="Dictionary of resource capacities"
    ),
    task_requirements: Dict[str, Dict[str, float]] = Field(
        description="Dictionary of task requirements per resource"
    ),
    task_priorities: Optional[Dict[str, float]] = Field(
        default=None, description="Optional dictionary of task priorities"
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Create a resource allocation optimization problem.
    """
    return create_resource_allocation_problem(
        resources, tasks, resource_capacities, task_requirements, task_priorities
    )


@mcp.tool
async def create_supply_chain_optimization_tool(
    suppliers: List[str] = Field(description="List of suppliers"),
    warehouses: List[str] = Field(description="List of warehouses"),
    customers: List[str] = Field(description="List of customers"),
    supplier_capacities: Dict[str, float] = Field(
        description="Dictionary of supplier capacities"
    ),
    warehouse_capacities: Dict[str, float] = Field(
        description="Dictionary of warehouse capacities"
    ),
    customer_demands: Dict[str, float] = Field(
        description="Dictionary of customer demands"
    ),
    transportation_costs: Dict[str, Dict[str, float]] = Field(
        description="Dictionary of transportation costs between locations"
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Create a supply chain optimization problem.
    """
    return create_supply_chain_optimization(
        suppliers,
        warehouses,
        customers,
        supplier_capacities,
        warehouse_capacities,
        customer_demands,
        transportation_costs,
    )


@mcp.tool
async def validate_optimization_problem_tool(
    problem_schema: Dict[str, Any] = Field(
        description="The optimization problem schema to validate"
    ),
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Validate an optimization problem schema.
    """
    return validate_optimization_problem(problem_schema)
