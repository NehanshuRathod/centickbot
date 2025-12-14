from mcp.server.fastmcp import FastMCP

from tools.booking import register_booking_tools
from tools.refund import register_refund_tools
from tools.support import register_support_tools

mcp = FastMCP(
    name="booking-mcp-server"
)

register_booking_tools(mcp)
register_refund_tools(mcp)
register_support_tools(mcp)

if __name__ == "__main__":
    mcp.run()
