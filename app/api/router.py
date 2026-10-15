from fastapi import APIRouter
from app.api.routes import health, products, auth, orders, invoices
api_router=APIRouter()
api_router.include_router(health.router,tags=["Sistema"])
api_router.include_router(products.router,prefix="/productos",tags=["Productos"])
api_router.include_router(auth.router,prefix="/auth",tags=["Autenticacion"])
api_router.include_router(orders.router,prefix="/pedidos",tags=["Pedidos"])
api_router.include_router(invoices.router,prefix="/facturas",tags=["Facturas"])
