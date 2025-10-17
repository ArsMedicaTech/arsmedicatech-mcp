Add the .env based off .env.example
.\.venv\Scripts\activate
for local
python local_mcp.py
for prod
python lib/llm/mcp/mcp_server.py