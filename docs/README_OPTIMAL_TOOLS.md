# Optimal Service Tools

This module provides experimental tools for mathematical optimization as a service, integrating with the Optimal API for solving various types of optimization problems including linear programming, portfolio optimization, resource allocation, and supply chain optimization.

## Functions

### `create_linear_optimization_problem(objective_type: str, variables: List[Dict], constraints: List[Dict], parameters: Optional[Dict] = None) -> Dict[str, Any]`

Creates a linear optimization problem for the Optimal service.

**Parameters:**
- `objective_type`: Type of optimization ('minimize' or 'maximize')
- `variables`: List of variable definitions with bounds
- `constraints`: List of constraint definitions
- `parameters`: Optional parameters for the optimization

**Returns:**
- Dictionary containing the optimization problem schema

**Example:**
```python
from lib.llm.mcp.tools.optimal import create_linear_optimization_problem

variables = [
    {"name": "x1", "type": "continuous", "lower_bound": 0.0, "upper_bound": 10.0},
    {"name": "x2", "type": "continuous", "lower_bound": 0.0, "upper_bound": 10.0}
]
constraints = [
    {
        "type": "inequality",
        "expression": "x1 + x2 <= 5",
        "description": "Sum constraint"
    }
]

problem = create_linear_optimization_problem("minimize", variables, constraints)
```

### `solve_optimization_problem(problem_schema: Dict[str, Any], api_key: str, timeout: int = 30) -> Dict[str, Any]`

Solves an optimization problem using the Optimal service.

**Parameters:**
- `problem_schema`: The optimization problem schema
- `api_key`: API key for the Optimal service
- `timeout`: Request timeout in seconds (default: 30)

**Returns:**
- Dictionary containing the optimization results

**Example:**
```python
from lib.llm.mcp.tools.optimal import solve_optimization_problem

result = solve_optimization_problem(problem, "your_api_key")
# Returns: {
#   "status": "success",
#   "optimal_value": 42.0,
#   "optimal_variables": [1.0, 2.0, 3.0],
#   "solver_info": {...}
# }
```

### `create_portfolio_optimization(assets: List[str], expected_returns: List[float], covariance_matrix: List[List[float]], target_return: Optional[float] = None, risk_free_rate: float = 0.02) -> Dict[str, Any]`

Creates a portfolio optimization problem (Markowitz model).

**Parameters:**
- `assets`: List of asset names
- `expected_returns`: List of expected returns for each asset
- `covariance_matrix`: Covariance matrix for asset returns
- `target_return`: Optional target return constraint
- `risk_free_rate`: Risk-free rate (default: 0.02)

**Returns:**
- Dictionary containing the portfolio optimization problem

**Example:**
```python
from lib.llm.mcp.tools.optimal import create_portfolio_optimization

assets = ["AAPL", "GOOGL", "MSFT"]
expected_returns = [0.08, 0.12, 0.10]
covariance_matrix = [
    [0.04, 0.02, 0.01],
    [0.02, 0.09, 0.03],
    [0.01, 0.03, 0.06]
]

portfolio = create_portfolio_optimization(assets, expected_returns, covariance_matrix, target_return=0.09)
```

### `create_resource_allocation_problem(resources: List[str], tasks: List[str], resource_capacities: Dict[str, float], task_requirements: Dict[str, Dict[str, float]], task_priorities: Optional[Dict[str, float]] = None) -> Dict[str, Any]`

Creates a resource allocation optimization problem.

**Parameters:**
- `resources`: List of available resources
- `tasks`: List of tasks to be allocated
- `resource_capacities`: Dictionary of resource capacities
- `task_requirements`: Dictionary of task requirements per resource
- `task_priorities`: Optional dictionary of task priorities

**Returns:**
- Dictionary containing the resource allocation problem

**Example:**
```python
from lib.llm.mcp.tools.optimal import create_resource_allocation_problem

resources = ["CPU", "Memory", "Storage"]
tasks = ["Task1", "Task2", "Task3"]
resource_capacities = {"CPU": 100.0, "Memory": 512.0, "Storage": 1000.0}
task_requirements = {
    "Task1": {"CPU": 20.0, "Memory": 64.0, "Storage": 100.0},
    "Task2": {"CPU": 30.0, "Memory": 128.0, "Storage": 200.0}
}

allocation = create_resource_allocation_problem(resources, tasks, resource_capacities, task_requirements)
```

### `create_supply_chain_optimization(suppliers: List[str], warehouses: List[str], customers: List[str], supplier_capacities: Dict[str, float], warehouse_capacities: Dict[str, float], customer_demands: Dict[str, float], transportation_costs: Dict[str, Dict[str, float]]) -> Dict[str, Any]`

Creates a supply chain optimization problem.

**Parameters:**
- `suppliers`: List of suppliers
- `warehouses`: List of warehouses
- `customers`: List of customers
- `supplier_capacities`: Dictionary of supplier capacities
- `warehouse_capacities`: Dictionary of warehouse capacities
- `customer_demands`: Dictionary of customer demands
- `transportation_costs`: Dictionary of transportation costs between locations

**Returns:**
- Dictionary containing the supply chain optimization problem

**Example:**
```python
from lib.llm.mcp.tools.optimal import create_supply_chain_optimization

suppliers = ["Supplier1", "Supplier2"]
warehouses = ["Warehouse1", "Warehouse2"]
customers = ["Customer1", "Customer2"]
supplier_capacities = {"Supplier1": 500.0, "Supplier2": 600.0}
warehouse_capacities = {"Warehouse1": 400.0, "Warehouse2": 450.0}
customer_demands = {"Customer1": 100.0, "Customer2": 150.0}
transportation_costs = {
    "Supplier1": {"Warehouse1": 10.0, "Warehouse2": 15.0},
    "Supplier2": {"Warehouse1": 12.0, "Warehouse2": 8.0}
}

supply_chain = create_supply_chain_optimization(
    suppliers, warehouses, customers, supplier_capacities,
    warehouse_capacities, customer_demands, transportation_costs
)
```

### `validate_optimization_problem(problem_schema: Dict[str, Any]) -> Dict[str, Any]`

Validates an optimization problem schema.

**Parameters:**
- `problem_schema`: The optimization problem schema to validate

**Returns:**
- Dictionary containing validation results

**Example:**
```python
from lib.llm.mcp.tools.optimal import validate_optimization_problem

validation = validate_optimization_problem(problem)
# Returns: {
#   "is_valid": True,
#   "errors": [],
#   "warnings": []
# }
```

## MCP Integration

The functions are also available as MCP tools when the MCP framework is available:

- `create_linear_optimization_problem_tool`: MCP tool for creating linear optimization problems
- `solve_optimization_problem_tool`: MCP tool for solving optimization problems
- `create_portfolio_optimization_tool`: MCP tool for portfolio optimization
- `create_resource_allocation_problem_tool`: MCP tool for resource allocation
- `create_supply_chain_optimization_tool`: MCP tool for supply chain optimization
- `validate_optimization_problem_tool`: MCP tool for problem validation

## Dependencies

The functions require the `amt_nano.services.optimal` module to be available. If the service is not available, the functions will return placeholder data.

## Testing

Run the test script to see the functions in action:

```bash
python test_optimal_tools.py
```

## Error Handling

All functions include proper error handling and will return fallback data if the Optimal service is not available or encounters errors. The functions log warnings and errors using the configured logger.

## Integration with Optimal Service

The functions integrate with the Optimal API which provides:

1. **Linear Programming**: Standard linear optimization problems
2. **Quadratic Programming**: Portfolio optimization and other quadratic problems
3. **Mixed Integer Programming**: Problems with discrete variables
4. **Constraint Programming**: Complex constraint satisfaction problems

## Problem Types Supported

### 1. **Linear Optimization**
- Standard linear programming problems
- Minimize or maximize linear objective functions
- Linear equality and inequality constraints

### 2. **Portfolio Optimization (Markowitz Model)**
- Asset allocation optimization
- Risk-return trade-off analysis
- Target return constraints
- Covariance-based risk modeling

### 3. **Resource Allocation**
- Multi-resource allocation problems
- Capacity constraints
- Task requirements and priorities
- Efficiency maximization

### 4. **Supply Chain Optimization**
- Multi-echelon supply chain networks
- Transportation cost minimization
- Capacity and demand constraints
- Flow optimization

## Configuration

For production use, you'll need to configure:

1. **API Key**: For Optimal service authentication
2. **Timeout Settings**: Based on problem complexity
3. **Solver Selection**: Choose appropriate solver for problem type

## Use Cases

These tools are particularly useful for:

- **Financial Planning**: Portfolio optimization and asset allocation
- **Operations Research**: Resource allocation and scheduling
- **Supply Chain Management**: Network optimization and logistics
- **Manufacturing**: Production planning and capacity optimization
- **Transportation**: Route optimization and fleet management
- **Energy**: Power generation and distribution optimization

## Mathematical Formulations

### Portfolio Optimization
```
Minimize: w^T Σ w
Subject to: w^T μ ≥ R_target
           Σ w_i = 1
           0 ≤ w_i ≤ 1
```

### Resource Allocation
```
Maximize: Σ Σ c_ij x_ij
Subject to: Σ x_ij ≤ C_i (capacity constraints)
           Σ x_ij ≥ R_j (requirement constraints)
           x_ij ≥ 0
```

### Supply Chain Optimization
```
Minimize: Σ Σ c_ij x_ij
Subject to: Σ x_ij ≤ S_i (supplier capacity)
           Σ x_ij ≤ W_j (warehouse capacity)
           Σ x_jk = D_k (customer demand)
           x_ij ≥ 0
```

## Best Practices

1. **Problem Formulation**: Ensure constraints are mathematically sound
2. **Variable Bounds**: Set appropriate bounds for numerical stability
3. **Constraint Scaling**: Scale constraints to avoid numerical issues
4. **Initial Guesses**: Provide good initial solutions when possible
5. **Validation**: Always validate problem schemas before solving 