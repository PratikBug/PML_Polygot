"""Tests for Vercel serverless entry point."""

def test_mangum_handler_is_exported():
    from index import handler
    assert handler is not None


def test_handler_responds_to_health():
    from index import handler

    event = {
        "version": "2.0",
        "routeKey": "GET /health",
        "rawPath": "/health",
        "rawQueryString": "",
        "headers": {},
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/health",
                "sourceIp": "127.0.0.1",
            }
        },
        "isBase64Encoded": False,
    }
    response = handler(event, None)
    assert response["statusCode"] == 200
    assert "ok" in response["body"]
