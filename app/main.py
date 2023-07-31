import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.v1.api import api_router as v1_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s",
    level=logging.DEBUG,
    datefmt="%d.%m.%Y %I:%M:%S"
)
logger = logging.getLogger("fast-api.info")

app = FastAPI()

# App specific routes
app.include_router(v1_router)

origins = [
    "http://0.0.0.0:8088",
    "http://localhost:8088",
    "http://localhost:8088",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Need to update this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test_api")
def read_main():
    return {"msg": "Hello World"}


@app.on_event("shutdown")
def shutdown_event():
    print("Application Shutdown")
    return {"msg": "Hello World"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="A POC for fastapi-postgresql -- OpenAPI documentation",
        version="v0.1.0",
        description="<h3>Misc Content</h3>"
                    + "<ol><li>This is OpenAPI (v3), a playground for the APIs</li>"
                    + "<li>Switch to <a href='/redoc'>redoc</a> for a standard API documentation</li></ol>"
                    + "</ul>",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# if __name__=="__main__":
#     uvicorn.run("app.app:app",host='0.0.0.0', port=8090, reload=True, debug=True, workers=3)
