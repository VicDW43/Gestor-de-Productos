
import sqlite3
from pathlib import Path

from modelo import Producto

RUTA_DB: Path = Path(__file__).parent / "productos.db"


def conectar(ruta: str | Path = RUTA_DB) -> sqlite3.Connection:
   
    conexion = sqlite3.connect(ruta)

    conexion.create_function("casefold", 1, str.casefold, deterministic=True)
    return conexion


def crear_tabla(conexion: sqlite3.Connection) -> None:
    with conexion: 
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio INTEGER NOT NULL
            )
        """)


def _fila_a_producto(fila: tuple[object, ...]) -> Producto:
    if len(fila) == 4:
        id_, nombre, categoria, precio = fila
        if (
            isinstance(id_, int)
            and isinstance(nombre, str)
            and isinstance(categoria, str)
            and isinstance(precio, int)
        ):
            return Producto(id_, nombre, categoria, precio)
    raise ValueError(f"La base devolvió una fila con formato inesperado: {fila!r}")


def agregar(
    conexion: sqlite3.Connection, nombre: str, categoria: str, precio: int
) -> Producto:
    """Reemplaza a: productos.append([nombre, categoria, precio])"""
    with conexion:
        cursor = conexion.execute(
            "INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)",
            (nombre, categoria, precio),  
        )
    nuevo_id = cursor.lastrowid
    if nuevo_id is None:
        raise RuntimeError("SQLite no devolvió el id del producto nuevo.")
    return Producto(nuevo_id, nombre, categoria, precio)


def listar(conexion: sqlite3.Connection) -> list[Producto]:
    """Reemplaza a: la lista `productos` completa (opciones 2 y 4)."""
    filas: list[tuple[object, ...]] = conexion.execute(
        "SELECT id, nombre, categoria, precio FROM productos ORDER BY id"
    ).fetchall()
    return [_fila_a_producto(fila) for fila in filas]


def buscar(conexion: sqlite3.Connection, termino: str) -> list[Producto]:
    filas: list[tuple[object, ...]] = conexion.execute(
        "SELECT id, nombre, categoria, precio FROM productos "
        "WHERE instr(casefold(nombre), ?) > 0 ORDER BY id",
        (termino.casefold(),),
    ).fetchall()
    return [_fila_a_producto(fila) for fila in filas]


def obtener(conexion: sqlite3.Connection, id_producto: int) -> Producto | None:
    fila: tuple[object, ...] | None = conexion.execute(
        "SELECT id, nombre, categoria, precio FROM productos WHERE id = ?",
        (id_producto,),
    ).fetchone()
    if fila is None:
        return None
    return _fila_a_producto(fila)


def quitar(conexion: sqlite3.Connection, id_producto: int) -> bool:
    with conexion:
        cursor = conexion.execute(
            "DELETE FROM productos WHERE id = ?", (id_producto,)
        )
    return cursor.rowcount > 0