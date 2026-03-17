from fastapi import FastAPI, Request
from src.endpoints import main as auth_v1
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import time

def create_application() -> FastAPI:
    application = FastAPI(
        title="Library platform",
        description="Library Auth Service.",
        version="1.0.0",
        openapi_url="/auth/openapi.json",
        docs_url="/auth/docs")
    application.include_router(auth_v1.router, prefix='/auth')
    return application

app = create_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-App"] = "Time took to process the request and return response is {} sec".format(time.time() - start_time)
    return response

@app.get('/')
def index():
    return RedirectResponse("/auth/docs")