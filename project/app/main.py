from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from app.api import auth, profile, products, cart, order

app = FastAPI(title="Flight Booking API")

app.include_router(auth.router, prefix="/api-flight", tags=["auth"])
app.include_router(profile.router, prefix="/api-flight", tags=["profile"])
app.include_router(products.router, prefix="/api-flight", tags=["products"])
app.include_router(cart.router, prefix="/api-flight", tags=["cart"])
app.include_router(order.router, prefix="/api-flight", tags=["order"])


@app.get("/api-flight/logout")
def logout():
    return {"message": "logout"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]
        errors[field] = "Validation error"
    return JSONResponse(status_code=422, content={"message": "Validation error", **errors})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

