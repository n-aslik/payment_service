from fastapi import FastAPI, Request, status
from fastapi.responses import Response
from src.endpoints import payment_routes as paid_v1
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import time
import pika
from contextlib import asynccontextmanager
from connections.dbconn import pg_pool, connection
from lib.config import get_rabbitmq_connection

@asynccontextmanager
async def lifespan (app: FastAPI):
    try:
        conn = pg_pool.getconn()
        pg_pool.putconn(conn)
        print("✅ Postgres pool ready")
    except Exception as e:
        raise RuntimeError(f"❌ Postgres not available: {e}")

    yield

    pg_pool.closeall()
    print("🔴 Postgres pool closed")




def create_application() -> FastAPI:
    application = FastAPI(
        title="Payment Service",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc")
    application.include_router(paid_v1.router)
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
    return RedirectResponse("/docs")

@app.get("/health")
async def health_check():
    health_status = {
        "status": "ok",
        "database": "down",
        "rabbitmq": "down",
    }
    overall_healthy = True

    try:
        with connection() as cur:
            cur.execute("SELECT 1")
            if cur.fetchone():
                health_status["database"] = "up"
    except Exception as e:
        health_status["status"] = "error"
        overall_healthy = False
        print(f"HealthCheck Database Error: {e}")


    try:
        
        params = pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=pika.PlainCredentials('guest', 'guest'), connection_attempts=1, retry_delay=1)
        connection_mq = pika.BlockingConnection(params)
        if connection_mq.is_open:
            health_status["rabbitmq"] = "up"
            connection_mq.close()
    except Exception as e:
        health_status["status"] = "error"
        overall_healthy = False
        print(f"HealthCheck RabbitMQ Error: {e}")

    # Если что-то не так, возвращаем 503 Service Unavailable
    return health_status if overall_healthy else Response(content=str(health_status), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)