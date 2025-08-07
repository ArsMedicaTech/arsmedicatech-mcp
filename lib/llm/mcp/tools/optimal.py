"""
Optimal Service tools for MCP server - Mathematical optimization as a service.
"""

from typing import Any, Dict, List, Optional, Union

from amt_nano.services.optimal import OptimalMetadata, OptimalSchema, OptimalService

from settings import logger


def create_linear_optimization_problem(
    objective_type: str,
    variables: List[Dict[str, Union[str, int]]],
    constraints: List[Dict[str, Any]],
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a linear optimization problem for the Optimal service.

    Args:
        objective_type: Type of optimization ('minimize' or 'maximize')
        variables: List of variable definitions with bounds
        constraints: List of constraint definitions
        parameters: Optional parameters for the optimization

    Returns:
        Dictionary containing the optimization problem schema
    """
    try:
        # Create metadata
        meta = OptimalMetadata(
            problem_id=f"linear_problem_{len(variables)}_vars",
            solver="linear_solver",
            sense=objective_type,
        )

        # Create objective function
        objective: Dict[str, Any] = {
            "type": "linear",
            "coefficients": [1.0] * len(variables),  # Default coefficients
        }

        # Create initial guess
        initial_guess = [0.0] * len(variables)

        # Create schema
        schema = OptimalSchema(
            meta=meta,
            variables=variables,
            parameters=parameters or {},
            objective=objective,
            constraints=constraints,
            initial_guess=initial_guess,
        )

        return schema.to_dict()

    except Exception as e:
        logger.error(f"Error creating linear optimization problem: {e}")
        return {"error": f"Failed to create optimization problem: {str(e)}"}


def solve_optimization_problem(
    problem_schema: Dict[str, Any], api_key: str, timeout: int = 30
) -> Dict[str, Any]:
    """
    Solve an optimization problem using the Optimal service.

    Args:
        problem_schema: The optimization problem schema
        api_key: API key for the Optimal service
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dictionary containing the optimization results
    """
    try:
        # Reconstruct the schema objects
        meta = OptimalMetadata(
            problem_id=problem_schema["meta"]["problem_id"],
            solver=problem_schema["meta"]["solver"],
            sense=problem_schema["meta"]["sense"],
        )

        schema = OptimalSchema(
            meta=meta,
            variables=problem_schema["variables"],
            parameters=problem_schema["parameters"],
            objective=problem_schema["objective"],
            constraints=problem_schema["constraints"],
            initial_guess=problem_schema["initial_guess"],
        )

        # Create service instance
        service = OptimalService(
            url="https://optimal.apphosting.services/optimize",
            api_key=api_key,
            schema=schema,
        )

        # Send the optimization problem
        result = service.send()

        return {
            "status": "success",
            "result": result,
            "problem_id": meta.problem_id,
            "solver": meta.solver,
        }

    except Exception as e:
        logger.error(f"Error solving optimization problem: {e}")
        return {
            "status": "error",
            "error": str(e),
            "problem_id": problem_schema.get("meta", {}).get("problem_id", "unknown"),
        }


def create_portfolio_optimization(
    assets: List[str],
    expected_returns: List[float],
    covariance_matrix: List[List[float]],
    target_return: Optional[float] = None,
    risk_free_rate: float = 0.02,
) -> Dict[str, Any]:
    """
    Create a portfolio optimization problem (Markowitz model).

    Args:
        assets: List of asset names
        expected_returns: List of expected returns for each asset
        covariance_matrix: Covariance matrix for asset returns
        target_return: Optional target return constraint
        risk_free_rate: Risk-free rate (default: 0.02)

    Returns:
        Dictionary containing the portfolio optimization problem
    """
    # Define variables (portfolio weights)
    variables: List[Dict[str, Union[str, int]]] = []
    for asset in assets:
        variables.append(
            {
                "name": f"weight_{asset}",
                "type": "continuous",
                "lower_bound": 0,
                "upper_bound": 1,
            }
        )

    # Define constraints
    constraints: List[Dict[str, Any]] = [
        {
            "type": "equality",
            "expression": " + ".join([f"weight_{asset}" for asset in assets])
            + " = 1.0",
            "description": "Portfolio weights sum to 1",
        }
    ]

    # Add target return constraint if specified
    if target_return is not None:
        return_constraint = {
            "type": "inequality",
            "expression": " + ".join(
                [
                    f"{expected_returns[i]} * weight_{asset}"
                    for i, asset in enumerate(assets)
                ]
            )
            + f" >= {target_return}",
            "description": f"Target return constraint: {target_return}",
        }
        constraints.append(return_constraint)

    # Create problem schema
    problem = create_linear_optimization_problem(
        objective_type="minimize",
        variables=variables,
        constraints=constraints,
        parameters={
            "assets": assets,
            "expected_returns": expected_returns,
            "covariance_matrix": covariance_matrix,
            "risk_free_rate": risk_free_rate,
            "target_return": target_return,
        },
    )

    return {
        "problem": problem,
        "assets": assets,
        "expected_returns": expected_returns,
        "target_return": target_return,
        "type": "portfolio_optimization",
    }


def create_resource_allocation_problem(
    resources: List[str],
    tasks: List[str],
    resource_capacities: Dict[str, float],
    task_requirements: Dict[str, Dict[str, float]],
    task_priorities: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Create a resource allocation optimization problem.

    Args:
        resources: List of available resources
        tasks: List of tasks to be allocated
        resource_capacities: Dictionary of resource capacities
        task_requirements: Dictionary of task requirements per resource
        task_priorities: Optional dictionary of task priorities

    Returns:
        Dictionary containing the resource allocation problem
    """
    # Define variables (allocation amounts)
    variables: List[Dict[str, Union[str, int]]] = []
    for task in tasks:
        for resource in resources:
            variables.append(
                {
                    "name": f"allocation_{task}_{resource}",
                    "type": "continuous",
                    "lower_bound": 0,
                    "upper_bound": int(resource_capacities.get(resource, 100.0)),
                }
            )

    # Define constraints
    constraints: List[Dict[str, Any]] = []

    # Resource capacity constraints
    for resource in resources:
        capacity = resource_capacities.get(resource, 100.0)
        task_terms = [f"allocation_{task}_{resource}" for task in tasks]
        sum_expression = " + ".join(task_terms)
        constraint = {
            "type": "inequality",
            "expression": f"{sum_expression} <= {capacity}",
            "description": f"Resource {resource} capacity constraint",
        }
        constraints.append(constraint)

    # Task requirement constraints
    for task in tasks:
        for resource in resources:
            requirement = task_requirements.get(task, {}).get(resource, 0.0)
            if requirement > 0:
                constraint = {
                    "type": "inequality",
                    "expression": f"allocation_{task}_{resource} >= {requirement}",
                    "description": f"Task {task} minimum requirement for {resource}",
                }
                constraints.append(constraint)

    # Create problem schema
    problem = create_linear_optimization_problem(
        objective_type="maximize",
        variables=variables,
        constraints=constraints,
        parameters={
            "resources": resources,
            "tasks": tasks,
            "resource_capacities": resource_capacities,
            "task_requirements": task_requirements,
            "task_priorities": task_priorities or {},
        },
    )

    return {
        "problem": problem,
        "resources": resources,
        "tasks": tasks,
        "type": "resource_allocation",
    }


def create_supply_chain_optimization(
    suppliers: List[str],
    warehouses: List[str],
    customers: List[str],
    supplier_capacities: Dict[str, float],
    warehouse_capacities: Dict[str, float],
    customer_demands: Dict[str, float],
    transportation_costs: Dict[str, Dict[str, float]],
) -> Dict[str, Any]:
    """
    Create a supply chain optimization problem.

    Args:
        suppliers: List of suppliers
        warehouses: List of warehouses
        customers: List of customers
        supplier_capacities: Dictionary of supplier capacities
        warehouse_capacities: Dictionary of warehouse capacities
        customer_demands: Dictionary of customer demands
        transportation_costs: Dictionary of transportation costs between locations

    Returns:
        Dictionary containing the supply chain optimization problem
    """
    # Define variables (flow amounts)
    variables: List[Dict[str, Union[str, int]]] = []

    # Supplier to warehouse flows
    for supplier in suppliers:
        for warehouse in warehouses:
            variables.append(
                {
                    "name": f"flow_supplier_{supplier}_warehouse_{warehouse}",
                    "type": "continuous",
                    "lower_bound": 0,
                    "upper_bound": int(supplier_capacities.get(supplier, 1000.0)),
                }
            )

    # Warehouse to customer flows
    for warehouse in warehouses:
        for customer in customers:
            variables.append(
                {
                    "name": f"flow_warehouse_{warehouse}_customer_{customer}",
                    "type": "continuous",
                    "lower_bound": 0,
                    "upper_bound": int(warehouse_capacities.get(warehouse, 1000.0)),
                }
            )

    # Define constraints
    constraints: List[Dict[str, Any]] = []

    # Supplier capacity constraints
    for supplier in suppliers:
        capacity = supplier_capacities.get(supplier, 1000.0)
        # Build the sum expression for all warehouses
        warehouse_terms = [
            f"flow_supplier_{supplier}_warehouse_{w}" for w in warehouses
        ]
        sum_expression = " + ".join(warehouse_terms)
        constraint = {
            "type": "inequality",
            "expression": f"{sum_expression} <= {capacity}",
            "description": f"Supplier {supplier} capacity constraint",
        }
        constraints.append(constraint)

    # Warehouse capacity constraints
    for warehouse in warehouses:
        capacity = warehouse_capacities.get(warehouse, 1000.0)
        # Build the sum expression for all customers
        customer_terms = [f"flow_warehouse_{warehouse}_customer_{c}" for c in customers]
        sum_expression = " + ".join(customer_terms)
        constraint = {
            "type": "inequality",
            "expression": f"{sum_expression} <= {capacity}",
            "description": f"Warehouse {warehouse} capacity constraint",
        }
        constraints.append(constraint)

    # Customer demand constraints
    for customer in customers:
        demand = customer_demands.get(customer, 0.0)
        # Build the sum expression for all warehouses
        warehouse_terms = [
            f"flow_warehouse_{w}_customer_{customer}" for w in warehouses
        ]
        sum_expression = " + ".join(warehouse_terms)
        constraint = {
            "type": "equality",
            "expression": f"{sum_expression} = {demand}",
            "description": f"Customer {customer} demand constraint",
        }
        constraints.append(constraint)

    # Create problem schema
    problem = create_linear_optimization_problem(
        objective_type="minimize",
        variables=variables,
        constraints=constraints,
        parameters={
            "suppliers": suppliers,
            "warehouses": warehouses,
            "customers": customers,
            "supplier_capacities": supplier_capacities,
            "warehouse_capacities": warehouse_capacities,
            "customer_demands": customer_demands,
            "transportation_costs": transportation_costs,
        },
    )

    return {
        "problem": problem,
        "suppliers": suppliers,
        "warehouses": warehouses,
        "customers": customers,
        "type": "supply_chain_optimization",
    }


def validate_optimization_problem(problem_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate an optimization problem schema.

    Args:
        problem_schema: The optimization problem schema to validate

    Returns:
        Dictionary containing validation results
    """
    validation_result: Dict[str, Any] = {"is_valid": True, "errors": [], "warnings": []}

    try:
        # Check required fields
        required_fields = [
            "meta",
            "variables",
            "objective",
            "constraints",
            "initial_guess",
        ]
        for field in required_fields:
            if field not in problem_schema:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Missing required field: {field}")

        # Check meta fields
        if "meta" in problem_schema:
            meta = problem_schema["meta"]
            meta_fields = ["problem_id", "solver", "sense"]
            for field in meta_fields:
                if field not in meta:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append(f"Missing meta field: {field}")

        # Check variables
        if "variables" in problem_schema:
            variables: List[Dict[str, Any]] = problem_schema["variables"]
            if len(variables) == 0:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Variables must be a non-empty list")

            # Check variable structure
            for i, var in enumerate(variables):
                if "name" not in var:
                    validation_result["errors"].append(
                        f"Variable {i} missing 'name' field"
                    )
                elif "type" not in var:
                    validation_result["errors"].append(
                        f"Variable {i} missing 'type' field"
                    )

        # Check constraints
        if "constraints" in problem_schema:
            constraints = problem_schema["constraints"]
            if not isinstance(constraints, list):
                validation_result["is_valid"] = False
                validation_result["errors"].append("Constraints must be a list")

        # Check initial guess
        if "initial_guess" in problem_schema:
            initial_guess: List[Any] = problem_schema["initial_guess"]
            if len(initial_guess) != len(problem_schema.get("variables", [])):
                validation_result["warnings"].append(
                    "Initial guess length doesn't match number of variables"
                )

        # Check objective
        if "objective" in problem_schema:
            objective = problem_schema["objective"]
            if not isinstance(objective, dict):
                validation_result["is_valid"] = False
                validation_result["errors"].append("Objective must be a dictionary")
            elif "type" not in objective:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Objective missing 'type' field")

    except Exception as e:
        validation_result["is_valid"] = False
        validation_result["errors"].append(f"Validation error: {str(e)}")

    return validation_result


# Export functions for use in other modules
__all__ = [
    "create_linear_optimization_problem",
    "solve_optimization_problem",
    "create_portfolio_optimization",
    "create_resource_allocation_problem",
    "create_supply_chain_optimization",
    "validate_optimization_problem",
]
