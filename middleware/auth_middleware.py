from fastapi import HTTPException, Header
import jwt
def auth_middleware(x_auth_token = Header()):
    try:
        if not x_auth_token:
            raise HTTPException(status_code=401, detail="Missing x-auth-token header")
        verified_token = jwt.decode(x_auth_token, "secret", algorithms=["HS256"])
        if not verified_token:
            raise HTTPException(status_code=401, detail="Invalid x-auth-token header")
        id = verified_token.get("id")
        if not id:
            raise HTTPException(status_code=401, detail="Invalid x-auth-token header")
        return {"id": id, "x_auth_token": x_auth_token}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid x-auth-token header")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))