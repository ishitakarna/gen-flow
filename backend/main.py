from fastapi import FastAPI
from starlette.requests import Request
from fastapi.responses import JSONResponse
from .routers import user_router, wf_router, process_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# @app.exception_handler(Exception)
# async def exception_callback(request: Request, exc: Exception):
#     return JSONResponse(content={"data": str(exc)}, status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(wf_router.router)
app.include_router(process_router.router)



