"""
MCP server entry point.
"""

import datetime

# Import all tool modules to ensure their registrations execute
# The import chain will ensure they all use the same mcp instance from mcp_init
from tools import (  # noqa: F401
    mcp_api_tools,
    mcp_bayesian_tools,
    mcp_icd_tools,
    mcp_medgemma_tools,
    mcp_optimal_tools,
)

# Import trees last to get the final mcp instance with all tools registered
from trees import mcp  # type: ignore

from settings import logger

if __name__ == "__main__":
    ts = datetime.datetime.now().isoformat()
    logger.debug(f"Starting MCP server at {ts}...")

    mcp.run(transport="http", host="0.0.0.0", port=9000, path="/mcp", log_level="debug")
