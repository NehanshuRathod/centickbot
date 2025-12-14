from mcp.server.fastmcp import FastMCP
from services.booking_service import BookingService

booking_service = BookingService()

def register_booking_tools(mcp: FastMCP):

    @mcp.tool(
        name="get_booking",
        description="Fetch booking details using booking ID"
    )
    def get_booking(booking_id: str):
        return booking_service.get_booking(booking_id)

    @mcp.tool(
        name="list_user_bookings",
        description="List all bookings for a user"
    )
    def list_user_bookings(user_id: str):
        return booking_service.list_user_bookings(user_id)

    @mcp.tool(
        name="cancel_booking",
        description="Cancel a booking and initiate refund if applicable"
    )
    def cancel_booking(booking_id: str, reason: str = "user_request"):
        return booking_service.cancel_booking(booking_id, reason)
