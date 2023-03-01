from http import HTTPStatus

from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header(default=None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="X-Token header invalid")
