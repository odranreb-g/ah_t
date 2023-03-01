from fastapi import Depends, FastAPI

from ah_t.dependencies import get_token_header
from ah_t.routers import car_owners

app = FastAPI(dependencies=[Depends(get_token_header)])

app.include_router(car_owners.router, prefix="/car-owners")
