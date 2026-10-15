from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Role(Base):
    __tablename__="Roles"
    RolID: Mapped[int]=mapped_column(Integer,primary_key=True)
    NombreRol: Mapped[str]=mapped_column(String(50),unique=True)
    Activo: Mapped[bool]=mapped_column(Boolean,default=True)

class User(Base):
    __tablename__="Usuarios"
    UsuarioID: Mapped[int]=mapped_column(Integer,primary_key=True)
    RolID: Mapped[int]=mapped_column(ForeignKey("Roles.RolID"))
    NombreUsuario: Mapped[str]=mapped_column(String(50),unique=True)
    Correo: Mapped[str]=mapped_column(String(150),unique=True)
    PasswordHash: Mapped[str]=mapped_column(String(500))
    Activo: Mapped[bool]=mapped_column(Boolean,default=True)
    CorreoVerificado: Mapped[bool]=mapped_column(Boolean,default=False)
    FechaCreacion: Mapped[datetime]=mapped_column(DateTime)
    role: Mapped[Role]=relationship()
    client: Mapped['Client|None']=relationship(back_populates="user",uselist=False)

class Client(Base):
    __tablename__="Clientes"
    ClienteID: Mapped[int]=mapped_column(Integer,primary_key=True)
    UsuarioID: Mapped[int|None]=mapped_column(ForeignKey("Usuarios.UsuarioID"),unique=True)
    Nombre: Mapped[str]=mapped_column(String(100))
    ApellidoPaterno: Mapped[str]=mapped_column(String(100))
    ApellidoMaterno: Mapped[str|None]=mapped_column(String(100))
    Telefono: Mapped[str|None]=mapped_column(String(20))
    Activo: Mapped[bool]=mapped_column(Boolean,default=True)
    user: Mapped[User|None]=relationship(back_populates="client")

class Category(Base):
    __tablename__="Categorias"
    CategoriaID: Mapped[int]=mapped_column(Integer,primary_key=True)
    Nombre: Mapped[str]=mapped_column(String(100))
    Slug: Mapped[str]=mapped_column(String(150),unique=True)
    Activa: Mapped[bool]=mapped_column(Boolean,default=True)

class Product(Base):
    __tablename__="Productos"
    ProductoID: Mapped[int]=mapped_column(Integer,primary_key=True)
    CategoriaID: Mapped[int]=mapped_column(ForeignKey("Categorias.CategoriaID"))
    SKU: Mapped[str]=mapped_column(String(50),unique=True)
    Nombre: Mapped[str]=mapped_column(String(150))
    Slug: Mapped[str]=mapped_column(String(180),unique=True)
    DescripcionCorta: Mapped[str|None]=mapped_column(String(300))
    Descripcion: Mapped[str|None]=mapped_column(Text)
    Precio: Mapped[Decimal]=mapped_column(Numeric(12,2))
    TiempoPreparacionMinutos: Mapped[int|None]=mapped_column(Integer)
    Destacado: Mapped[bool]=mapped_column(Boolean,default=False)
    Activo: Mapped[bool]=mapped_column(Boolean,default=True)
    category: Mapped[Category]=relationship()

class Branch(Base):
    __tablename__="Sucursales"
    SucursalID: Mapped[int]=mapped_column(Integer,primary_key=True)
    CodigoSucursal: Mapped[str]=mapped_column(String(20))
    Nombre: Mapped[str]=mapped_column(String(150))
    Activa: Mapped[bool]=mapped_column(Boolean,default=True)

class OrderStatus(Base):
    __tablename__="EstadosPedido"
    EstadoPedidoID: Mapped[int]=mapped_column(Integer,primary_key=True)
    Nombre: Mapped[str]=mapped_column(String(50),unique=True)

class Order(Base):
    __tablename__="Pedidos"
    PedidoID: Mapped[int]=mapped_column(BigInteger,primary_key=True)
    NumeroPedido: Mapped[str]=mapped_column(String(30),unique=True)
    ClienteID: Mapped[int|None]=mapped_column(ForeignKey("Clientes.ClienteID"))
    SucursalID: Mapped[int]=mapped_column(ForeignKey("Sucursales.SucursalID"))
    EstadoPedidoID: Mapped[int]=mapped_column(ForeignKey("EstadosPedido.EstadoPedidoID"))
    TipoEntrega: Mapped[str]=mapped_column(String(20))
    CanalVenta: Mapped[str]=mapped_column(String(20))
    FechaPedido: Mapped[datetime]=mapped_column(DateTime)
    Subtotal: Mapped[Decimal]=mapped_column(Numeric(12,2))
    Descuento: Mapped[Decimal]=mapped_column(Numeric(12,2))
    CostoEnvio: Mapped[Decimal]=mapped_column(Numeric(12,2))
    Impuestos: Mapped[Decimal]=mapped_column(Numeric(12,2))
    Total: Mapped[Decimal]=mapped_column(Numeric(12,2))
    status: Mapped[OrderStatus]=relationship()
    details: Mapped[list['OrderDetail']]=relationship(back_populates="order",cascade="all, delete-orphan")

class OrderDetail(Base):
    __tablename__="DetallePedido"
    DetallePedidoID: Mapped[int]=mapped_column(BigInteger,primary_key=True)
    PedidoID: Mapped[int]=mapped_column(ForeignKey("Pedidos.PedidoID"))
    ProductoID: Mapped[int]=mapped_column(ForeignKey("Productos.ProductoID"))
    NombreProducto: Mapped[str]=mapped_column(String(150))
    Cantidad: Mapped[int]=mapped_column(Integer)
    PrecioUnitario: Mapped[Decimal]=mapped_column(Numeric(12,2))
    Descuento: Mapped[Decimal]=mapped_column(Numeric(12,2),default=0)
    Impuestos: Mapped[Decimal]=mapped_column(Numeric(12,2),default=0)
    Subtotal: Mapped[Decimal]=mapped_column(Numeric(12,2))
    order: Mapped[Order]=relationship(back_populates="details")

class Invoice(Base):
    __tablename__="Facturas"
    FacturaID: Mapped[int]=mapped_column(BigInteger,primary_key=True)
    PedidoID: Mapped[int]=mapped_column(ForeignKey("Pedidos.PedidoID"))
    Folio: Mapped[int]=mapped_column(BigInteger)
    FechaEmision: Mapped[datetime]=mapped_column(DateTime)
    RFCReceptor: Mapped[str]=mapped_column(String(13))
    RazonSocialReceptor: Mapped[str]=mapped_column(String(250))
    Total: Mapped[Decimal]=mapped_column(Numeric(12,2))
    Estado: Mapped[str]=mapped_column(String(20))
