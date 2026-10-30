from openpyxl import load_workbook
from leer_xml import lee_factura
import uuid


def llenar_excel(lista,trabajador, obra):
    libro = load_workbook("COMPROBACION CLAUDE.xlsx")#Le decimos que cargue el libro o "workbook" abre el archivo en la memoria de python
    hoja = libro.active#Toma la hoja que esta activa, en este caso la unica que tenemos

    
    fila = 4#Declaramos que fila empieza a partir de 4
    for fac in lista:#hacemos un for para que recorra las facturas de nuestra lista anterior
        datos = lee_factura(fac)#lo guardamos en nuestra varible for, le decimos que cumpla nuestra funcion con la info captada del for(fac)

        #primero tomamos la variable "hoja" que es la que activamos anteriormente, y le señalamos la celda entre "corchetes" a la cual queremos que mande la informacion en nuestro archivo excel, 
        #despues del "=" le pasamos nuestras claves generadas en nuestro diccionario de "leer_xml" para que de ahi tome la información 
        hoja[(f"A{fila}")] = datos["fecha"] 
        hoja[(f"C{fila}")] = datos["uuid"]
        hoja[(f"D{fila}")] = datos["nombre"]
        hoja[(f"G{fila}")] = datos["subtotal"]
        hoja[(f"H{fila}")] = datos["iva"]
        hoja[(f"I{fila}")] = datos["ret_iva"]
        hoja[(f"J{fila}")] = datos["descuento"]
        hoja[(f"K{fila}")] = datos["otros_impuestos"]
        hoja[(f"M{fila}")] = datos["formapago"]
        hoja[(f"N{fila}")] = datos["descripcion"]
        hoja[(f"O{fila}")] = datos["rfc"]
        hoja[(f"B{fila}")] = "SI"
        hoja[(f"E{fila}")] = trabajador
        hoja[(f"F{fila}")] = obra

        fila = fila + 1

    nombre = f"Comprobacion_{uuid.uuid4().hex}.xlsx"
    ruta = f"Salidas/{nombre}"
    libro.save(ruta)
    return ruta

