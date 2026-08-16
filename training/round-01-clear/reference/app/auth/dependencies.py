from fastapi import HTTPException, Request

TEST_ACCOUNTS = {"demo": "demo1234"}


def authenticate(username: str, password: str) -> bool:
    """B5-3 allows a documented in-memory test account."""
    return TEST_ACCOUNTS.get(username) == password


def require_username(request: Request) -> str:
    """Protect a route through Depends().

    A missing session is answered with 303 + Location so a browser moves to /login.
    """
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return str(username)
