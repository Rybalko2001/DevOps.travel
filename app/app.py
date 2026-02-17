import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

ENV_NAME = os.getenv("ENV_NAME", "local")

@app.get("/healthz")
def healthz():
    return JSONResponse({
        "status": "ok",
        "service": "app",
        "env": ENV_NAME
    })