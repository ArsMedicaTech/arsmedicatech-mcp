"""
MCP server entry point.
"""

import datetime

from trees import mcp  # type: ignore

from settings import logger

if __name__ == "__main__":
    ts = datetime.datetime.now().isoformat()
    logger.debug(f"Starting MCP server at {ts}...")

    mcp.run(transport="http", host="0.0.0.0", port=9000, path="/mcp", log_level="debug")
