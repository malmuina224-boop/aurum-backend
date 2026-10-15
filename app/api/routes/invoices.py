from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.entities import User, Invoice, Order
router=APIRouter()
@router.get("/mis-facturas")
def mine(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not user.client: return []
    rows=db.execute(select(Invoice,Order.NumeroPedido).join(Order,Order.PedidoID==Invoice.PedidoID).where(Order.ClienteID==user.client.ClienteID).order_by(Invoice.FechaEmision.desc())).all()
    return [{"id":f.FacturaID,"pedido":number,"folio":f.Folio,"fecha":f.FechaEmision,"rfc":f.RFCReceptor,"razon_social":f.RazonSocialReceptor,"total":f.Total,"estado":f.Estado} for f,number in rows]
