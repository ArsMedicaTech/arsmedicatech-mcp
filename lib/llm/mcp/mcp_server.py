"""
MCP server entry point.
"""
import datetime

from trees import mcp  # type: ignore

from settings import logger

# --- import side‑effect modules that register tools ---
try:
    # These imports register the tools with the MCP framework
    from tools.mcp_icd_tools import (  # noqa: F401
        predict_icd_codes_tool,
        extract_medical_entities_tool,
        get_icd_code_details_tool,
        validate_icd_code_tool
    )
    logger.info("ICD Autocoder tools registered successfully")
except ImportError as e:
    logger.warning(f"Could not import ICD Autocoder tools: {e}")

try:
    # These imports register the API tools with the MCP framework
    from tools.mcp_api_tools import (  # noqa: F401
        fetch_medline_info_tool,
        fetch_clinical_trials_tool,
        fetch_pubmed_studies_tool,
        search_medical_literature_tool,
        get_medical_evidence_tool,
        validate_icd10_code_tool
    )
    logger.info("API service tools registered successfully")
except ImportError as e:
    logger.warning(f"Could not import API service tools: {e}")

try:
    # These imports register the Optimal tools with the MCP framework
    from tools.mcp_optimal_tools import (  # noqa: F401
        create_linear_optimization_problem_tool,
        solve_optimization_problem_tool,
        create_portfolio_optimization_tool,
        create_resource_allocation_problem_tool,
        create_supply_chain_optimization_tool,
        validate_optimization_problem_tool
    )
    logger.info("Optimal service tools registered successfully")
except ImportError as e:
    logger.warning(f"Could not import Optimal service tools: {e}")

try:
    # These imports register the MedGemma tools with the MCP framework
    from tools.mcp_medgemma_tools import (  # noqa: F401
        analyze_medical_image_tool,
        batch_analyze_medical_images_tool,
        validate_medical_image_url_tool
    )
    logger.info("MedGemma medical vision tools registered successfully")
except ImportError as e:
    logger.warning(f"Could not import MedGemma tools: {e}")

if __name__ == "__main__":
    ts = datetime.datetime.now().isoformat()
    logger.debug(f"Starting MCP server at {ts}...")

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=9000,
        path="/mcp",
        log_level="debug"
    )
