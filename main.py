import almacenamiento
import interfaz

def main() -> None:
    conexion = almacenamiento.conectar()  
    try:
        almacenamiento.crear_tabla(conexion)  
        while True:  
            interfaz.mostrar_menu()
            opcion = interfaz.pedir_opcion()

            if opcion == "1":  
                interfaz.opcion_agregar(conexion)
            elif opcion == "2":  
                interfaz.opcion_ver(conexion)
            elif opcion == "3":  
                interfaz.opcion_buscar(conexion)
            elif opcion == "4":  
                interfaz.opcion_eliminar(conexion)
            elif opcion == "5":  
                interfaz.mostrar_despedida()
                break
            else:  
                interfaz.mostrar_error("opción inválida. Elegí un número del 1 al 5.")
    except (KeyboardInterrupt, EOFError):  
        interfaz.mostrar_despedida()
    finally:
        conexion.close()  


if __name__ == "__main__":
    main()