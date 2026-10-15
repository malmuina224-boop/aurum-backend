from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.entities import User, Product, Branch, OrderStatus, Order, OrderDetail
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut
router=APIRouter()
def out(o): return OrderOut(id=o.PedidoID,number=o.NumeroPedido,status=o.status.Nombre,created_at=o.FechaPedido,total=o.Total,items=[OrderItemOut(product_id=d.ProductoID,name=d.NombreProducto,quantity=d.Cantidad,unit_price=d.PrecioUnitario,subtotal=d.Subtotal) for d in o.details])
@router.get("/mis-pedidos",response_model=list[OrderOut])
def mine(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not user.client: return []
    orders=db.scalars(select(Order).where(Order.ClienteID==user.client.ClienteID).order_by(Order.FechaPedido.desc())).unique().all()
    return [out(o) for o in orders]
@router.post("",response_model=OrderOut,status_code=201)
def create_order(data:OrderCreate,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not user.client: raise HTTPException(400,"El usuario no tiene perfil de cliente")
    if not data.items: raise HTTPException(400,"El pedido debe contener productos")
    if not db.get(Branch,data.branch_id): raise HTTPException(404,"Sucursal no encontrada")
    status=db.scalar(select(OrderStatus).where(OrderStatus.Nombre=="Pendiente de pago"))
    if not status: raise HTTPException(500,"Estado inicial no configurado")
    ids=[i.product_id for i in data.items]; products={p.ProductoID:p for p in db.scalars(select(Product).where(Product.ProductoID.in_(ids),Product.Activo==True)).all()}
    if len(products)!=len(set(ids)): raise HTTPException(400,"Uno o mas productos no existen o estan inactivos")
    subtotal=sum((products[i.product_id].Precio*i.quantity for i in data.items),Decimal("0")); impuestos=Decimal("0"); total=subtotal+data.shipping_cost
    order=Order(NumeroPedido="AUR-"+uuid4().hex[:12].upper(),ClienteID=user.client.ClienteID,SucursalID=data.branch_id,EstadoPedidoID=status.EstadoPedidoID,TipoEntrega=data.delivery_type,CanalVenta="WEB",FechaPedido=datetime.now(),Subtotal=subtotal,Descuento=0,CostoEnvio=data.shipping_cost,Impuestos=impuestos,Total=total)
    for item in data.items:
        p=products[item.product_id]; order.details.append(OrderDetail(ProductoID=p.ProductoID,NombreProducto=p.Nombre,Cantidad=item.quantity,PrecioUnitario=p.Precio,Descuento=0,Impuestos=0,Subtotal=p.Precio*item.quantity))
    db.add(order); db.commit(); db.refresh(order); return out(order)
