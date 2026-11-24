from dataclasses import dataclass

PRECIO_MAXIMO: int = 1_000_000_000


@dataclass(frozen=True)
class Producto:
    id: int  
    nombre: str  
    categoria: str  
    precio: int  