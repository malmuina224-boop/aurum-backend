from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Product, Category
from app.schemas.product import ProductOut
router=APIRouter()
def serialize(p): return ProductOut(id=p.ProductoID,sku=p.SKU,name=p.Nombre,slug=p.Slug,category=p.category.Nombre,description=p.DescripcionCorta or p.Descripcion,price=p.Precio,prep_minutes=p.TiempoPreparacionMinutos,featured=p.Destacado)
@router.get("",response_model=list[ProductOut])
def list_products(search:str|None=None,category:str|None=None,featured:bool|None=None,limit:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(Product).join(Product.category).where(Product.Activo==True,Category.Activa==True)
    if search: stmt=stmt.where(Product.Nombre.ilike(f"%{search}%"))
    if category: stmt=stmt.where(Category.Slug==category)
    if featured is not None: stmt=stmt.where(Product.Destacado==featured)
    return [serialize(p) for p in db.scalars(stmt.limit(limit)).all()]
@router.get("/{product_id}",response_model=ProductOut)
def get_product(product_id:int,db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p or not p.Activo: raise HTTPException(404,"Producto no encontrado")
    return serialize(p)
