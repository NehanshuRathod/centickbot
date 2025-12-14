from mcp.server.fastmcp import FastMCP
from services.refund_service import RefundService

refund_service = RefundService()

def register_refund_tools(mcp: FastMCP):

    @mcp.tool(
        name="get_refund_status",
        description="Get refund status for a booking"
    )
    def get_refund_status(booking_id: str):
        return refund_service.get_refund_status(booking_id)
