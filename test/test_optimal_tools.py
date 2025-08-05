#!/usr/bin/env python3
"""
Test script for Optimal service tools.
"""
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib.llm.mcp.tools.optimal import (create_linear_optimization_problem,
                                       create_portfolio_optimization,
                                       create_resource_allocation_problem,
                                       create_supply_chain_optimization,
                                       solve_optimization_problem,
                                       validate_optimization_problem)


def test_optimal_tools():
    """Test the Optimal service functions."""
    print("Testing Optimal Service Tools")
    print("=" * 50)
    
    # Test 1: Linear optimization problem
    print("1. Testing linear optimization problem creation:")
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
    print(f"   Problem ID: {problem.get('meta', {}).get('problem_id', 'N/A')}")
    print(f"   Variables: {len(problem.get('variables', []))}")
    print(f"   Constraints: {len(problem.get('constraints', []))}")
    print()
    
    # Test 2: Problem validation
    print("2. Testing problem validation:")
    validation = validate_optimization_problem(problem)
    print(f"   Is valid: {validation.get('is_valid', False)}")
    if validation.get('errors'):
        print(f"   Errors: {validation['errors']}")
    if validation.get('warnings'):
        print(f"   Warnings: {validation['warnings']}")
    print()
    
    # Test 3: Portfolio optimization
    print("3. Testing portfolio optimization:")
    assets = ["AAPL", "GOOGL", "MSFT"]
    expected_returns = [0.08, 0.12, 0.10]
    covariance_matrix = [
        [0.04, 0.02, 0.01],
        [0.02, 0.09, 0.03],
        [0.01, 0.03, 0.06]
    ]
    
    portfolio = create_portfolio_optimization(assets, expected_returns, covariance_matrix, target_return=0.09)
    print(f"   Assets: {portfolio.get('assets', [])}")
    print(f"   Target return: {portfolio.get('target_return', 'N/A')}")
    print(f"   Problem type: {portfolio.get('type', 'N/A')}")
    print()
    
    # Test 4: Resource allocation
    print("4. Testing resource allocation:")
    resources = ["CPU", "Memory", "Storage"]
    tasks = ["Task1", "Task2", "Task3"]
    resource_capacities = {"CPU": 100.0, "Memory": 512.0, "Storage": 1000.0}
    task_requirements = {
        "Task1": {"CPU": 20.0, "Memory": 64.0, "Storage": 100.0},
        "Task2": {"CPU": 30.0, "Memory": 128.0, "Storage": 200.0},
        "Task3": {"CPU": 25.0, "Memory": 96.0, "Storage": 150.0}
    }
    
    allocation = create_resource_allocation_problem(resources, tasks, resource_capacities, task_requirements)
    print(f"   Resources: {allocation.get('resources', [])}")
    print(f"   Tasks: {allocation.get('tasks', [])}")
    print(f"   Problem type: {allocation.get('type', 'N/A')}")
    print()
    
    # Test 5: Supply chain optimization
    print("5. Testing supply chain optimization:")
    suppliers = ["Supplier1", "Supplier2"]
    warehouses = ["Warehouse1", "Warehouse2"]
    customers = ["Customer1", "Customer2", "Customer3"]
    supplier_capacities = {"Supplier1": 500.0, "Supplier2": 600.0}
    warehouse_capacities = {"Warehouse1": 400.0, "Warehouse2": 450.0}
    customer_demands = {"Customer1": 100.0, "Customer2": 150.0, "Customer3": 200.0}
    transportation_costs = {
        "Supplier1": {"Warehouse1": 10.0, "Warehouse2": 15.0},
        "Supplier2": {"Warehouse1": 12.0, "Warehouse2": 8.0}
    }
    
    supply_chain = create_supply_chain_optimization(
        suppliers, warehouses, customers, supplier_capacities,
        warehouse_capacities, customer_demands, transportation_costs
    )
    print(f"   Suppliers: {supply_chain.get('suppliers', [])}")
    print(f"   Warehouses: {supply_chain.get('warehouses', [])}")
    print(f"   Customers: {supply_chain.get('customers', [])}")
    print(f"   Problem type: {supply_chain.get('type', 'N/A')}")
    print()
    
    # Test 6: Solve optimization problem (placeholder)
    print("6. Testing optimization problem solving:")
    api_key = "test_api_key"
    result = solve_optimization_problem(problem, api_key)
    print(f"   Status: {result.get('status', 'N/A')}")
    if result.get('status') == 'success':
        print(f"   Optimal value: {result.get('optimal_value', 'N/A')}")
        print(f"   Optimal variables: {result.get('optimal_variables', [])}")
    else:
        print(f"   Error: {result.get('error', 'N/A')}")
    print()
    
    print("All tests completed!")


if __name__ == "__main__":
    test_optimal_tools() 