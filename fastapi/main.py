from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from api.main import router as api_router

app = FastAPI(title="FastAPI REST API", description="A REST API", version="1.0.0")

app.include_router(api_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
