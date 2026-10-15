from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.api.router import api_router

app=FastAPI(title=settings.app_name,version="1.0.0",description="API REST para AURUM Sweet Alchemy")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(api_router,prefix=settings.api_v1_prefix)
@app.get("/")
def root(): return {"name":settings.app_name,"docs":"/docs","health":f"{settings.api_v1_prefix}/health"}
@app.exception_handler(SQLAlchemyError)
def db_error(_,exc): return JSONResponse(status_code=503,content={"detail":"No fue posible completar la operacion de base de datos"})
