# Booking MCP Server

This repository contains an **MCP (Model Context Protocol) server** for a booking-based chatbot system.

The MCP server exposes **well-defined tools** that an LLM can call to perform booking-related operations such as fetching bookings, cancelling bookings, checking refund status, and creating support tickets.

---

## Tasks to Be Completed by Backend / DB Integration 

This MCP server is **structurally complete**.  
The following tasks are intentionally left pending for database and backend integration.

 **Important:**  
Do **NOT** modify:
- Tool names
- Tool arguments
- MCP wiring (`server.py`)
- Tool registration logic

Only work inside the `services/` directory.

---

###  What Is Already Implemented

- MCP server setup using FastMCP
- Stable tool contracts for LLM integration
- Clean folder structure and separation of concerns
- Tool registration and MCP wiring

---

###  Pending Tasks

#### Database Integration

Implement database connectivity inside the `services/` layer.

Files to work on:

services/
├── booking_service.py

├── refund_service.py

└── support_service.py


## Architecture Overview

