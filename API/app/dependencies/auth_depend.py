from fastapi import Request, HTTPException


def auth_dependency(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != "Bearer valid-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
