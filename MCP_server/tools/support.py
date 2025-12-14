from mcp.server.fastmcp import FastMCP
from services.support_service import SupportService

support_service = SupportService()

def register_support_tools(mcp: FastMCP):

    @mcp.tool(
        name="create_support_ticket",
        description="Create a support ticket for human assistance"
    )
    def create_support_ticket(user_id: str, category: str, message: str):
        return support_service.create_ticket(user_id, category, message)
