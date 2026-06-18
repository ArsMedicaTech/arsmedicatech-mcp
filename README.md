Add the .env based off .env.example
.\.venv\Scripts\activate
for local
python local_mcp.py
for prod
python lib/llm/mcp/mcp_server.py

On newer versions of Python:

```bash
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
pip install pydantic-core
```