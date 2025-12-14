def error_response(code: str, message: str):
    return {
        "error": code,
        "message": message
    }
