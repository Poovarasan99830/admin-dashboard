from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy role extractor
def get_current_user_roles(token: str = Depends(oauth2_scheme)) -> List[str]:
    # 🔑 Accept only "admin-token" for now
    if token == "admin-token":
        return ["admin"]
    # any other token or missing token -> unauthorized
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
    )

def admin_required(roles: List[str] = Depends(get_current_user_roles)):
    if "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return True
