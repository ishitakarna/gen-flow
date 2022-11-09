from fastapi import FastAPI
from starlette.requests import Request
from fastapi.responses import JSONResponse
from .routers import test_router

app = FastAPI()

# @app.exception_handler(Exception)
# async def exception_callback(request: Request, exc: Exception):
#     return JSONResponse(content={"data": str(exc)}, status_code=500)

app.include_router(test_router.router)


