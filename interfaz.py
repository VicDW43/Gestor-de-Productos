from sqlite3 import Connection
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

import almacenamiento
from modelo import PRECIO_MAXIMO, Producto

consola: Console = Console()
ID_MAXIMO: int = 2**63 - 1  
def mostrar_error(mensaje: str) -> None:
    consola.print(f"[bold red]Error:[/bold red] {mensaje}")


def mostrar_exito(mensaje: str) -> None:
    consola.print(f"[bold green]{mensaje}[/bold green]")


def mostrar_aviso(mensaje: str) -> None:
    consola.print(f"[yellow]{mensaje}[/yellow]")


def mostrar_despedida() -> None:
    consola.print("\n[bold cyan]¡Hasta luego![/bold cyan]")  
def mostrar_menu() -> None:
   
    texto = (
        "[bold]1.[/bold] Agregar producto\n"
        "[bold]2.[/bold] Ver productos\n"
        "[bold]3.[/bold] Buscar producto\n"
        "[bold]4.[/bold] Eliminar producto\n"
        "[bold]5.[/bold] Salir"
    )
    consola.print()
    consola.print(
        Panel(
            texto,
            title="[bold cyan]GESTOR DE PRODUCTOS[/bold cyan]",
            expand=False,
            padding=(1, 4),
        )
    )


def pedir_opcion() -> str:
    
    return consola.input("[bold]Elegí una opción (1-5):[/bold] ").strip()


def pedir_texto(pregunta: str, mensaje_error: str) -> str:
    
    while True:
        texto = consola.input(f"{pregunta}: ").strip()
        if texto != "":
            return texto
        mostrar_error(mensaje_error)


def _con_puntos(numero: int) -> str:

    return f"{numero:,}".replace(",", ".")


def pedir_entero(pregunta: str, campo: str, minimo: int, maximo: int) -> int:
  
    while True:
        texto = consola.input(f"{pregunta}: ").strip()
        if texto == "":
            mostrar_error(f"{campo} no puede estar vacío.")
        elif not texto.isdecimal():
            mostrar_error(  "ingresá solo números enteros (sin puntos, comas ni signos)."  
            )

        elif len(texto) > len(str(maximo)) or not minimo <= int(texto) <= maximo:
            mostrar_error(
                f"{campo} debe estar entre {_con_puntos(minimo)} "
                f"y {_con_puntos(maximo)}."
            )
        else:
            return int(texto)


def confirmar(pregunta: str) -> bool:
    
    while True:
        respuesta = consola.input(f"{pregunta} (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        mostrar_error("respondé 's' o 'n'.")

def mostrar_productos(productos: list[Producto], titulo: str) -> None:
    tabla = Table(title=titulo, header_style="bold cyan")
    tabla.add_column("ID", justify="right")
    tabla.add_column("Nombre")
    tabla.add_column("Categoría")
    tabla.add_column("Precio", justify="right", style="green")
    for producto in productos:
        tabla.add_row(
            str(producto.id),
            escape(producto.nombre),
            escape(producto.categoria),
            f"${_con_puntos(producto.precio)}",
        )
    consola.print(tabla)



def opcion_agregar(conexion: Connection) -> None:
    consola.print("\n[bold]--- Agregar producto ---[/bold]")
    nombre = pedir_texto("Nombre del producto", "el nombre no puede estar vacío.")
    categoria = pedir_texto("Categoría", "la categoría no puede estar vacía.")
    precio = pedir_entero("Precio (sin centavos)", "el precio", 1, PRECIO_MAXIMO)
    almacenamiento.agregar(conexion, nombre, categoria, precio)  
    mostrar_exito(f"Producto '{escape(nombre)}' agregado correctamente.")


def opcion_ver(conexion: Connection) -> None:
    consola.print()
    productos = almacenamiento.listar(conexion)
    if len(productos) == 0:
        mostrar_aviso("Todavía no hay productos cargados.")
    else:
        mostrar_productos(productos, "Productos registrados")


def opcion_buscar(conexion: Connection) -> None:
    consola.print("\n[bold]--- Buscar producto ---[/bold]")
    if len(almacenamiento.listar(conexion)) == 0:
        mostrar_aviso("No hay productos cargados para buscar.")
        return
    termino = pedir_texto(
        "Ingresá el nombre a buscar", "el texto de búsqueda no puede estar vacío."
    )
    encontrados = almacenamiento.buscar(conexion, termino)
    if len(encontrados) == 0:
        mostrar_aviso("No se encontraron resultados.")
    else:
        mostrar_productos(encontrados, "Resultados")


def opcion_eliminar(conexion: Connection) -> None:
    consola.print("\n[bold]--- Eliminar producto ---[/bold]")
    productos = almacenamiento.listar(conexion)
    if len(productos) == 0:
        mostrar_aviso("No hay productos para eliminar.")
        return
    mostrar_productos(productos, "Productos registrados")

    id_producto = pedir_entero("ID del producto a eliminar", "el ID", 1, ID_MAXIMO)
    producto = almacenamiento.obtener(conexion, id_producto)  
    if producto is None:  
        mostrar_error(f"no existe ningún producto con ID {id_producto}.")
        return
    if not confirmar(f"¿Eliminar '{escape(producto.nombre)}'?"):
        mostrar_aviso("Operación cancelada.")
        return

    if almacenamiento.quitar(conexion, id_producto):  
        mostrar_exito(f"Producto '{escape(producto.nombre)}' eliminado correctamente.")
    else:
        mostrar_error("el producto ya no existe.")