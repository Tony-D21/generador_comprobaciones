import xml.etree.ElementTree as ET




ns = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}

def lee_factura(ruta):

    arbol = ET.parse (ruta)
    raiz = arbol.getroot()

    emisor = raiz.find("cfdi:Emisor",ns)
    timbre = raiz.find("cfdi:Complemento/tfd:TimbreFiscalDigital",ns)


    conceptos = raiz.findall("cfdi:Conceptos/cfdi:Concepto",ns)#creamos la variable impuestos y le decimos a que etiquetas del xml se debe ir(unas etiquetas estan dentro de otras)
    descripciones = []#creamos una lista donde importaremos los datos extraidos del xml
    for concepto in conceptos:#hacemos que recorra la informacion que esta dentro de las etiquetas que le pasamos, esto con un for
        descripciones.append(concepto.attrib["Descripcion"])#hasta que se encuentre la palabra "Importe", le decimos con .append que la agregue al diccionario (traslados)
    texto_conceptos = ", ".join(descripciones)#con .join, agregamos  una ", para que el texto no salga junto y darle forma

    #Aqui revisamos el iva
    impuestos = raiz.findall("cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado",ns)#creamos la variable impuestos y le decimos a que etiquetas del xml se debe ir(unas etiquetas estan dentro de otras)
    iva = 0
    otros_impuestos = 0#Agregamos otro diccionario para captar 
    for impuesto in impuestos:#hacemos que recorra la informacion que esta dentro de las etiquetas que le pasamos, esto con un for
        if impuesto.attrib["Impuesto"] == "002":#revisamos y validamos con un if que en la etiqueta "Traslado" exista un bloque "Impuesto" que su valor sea "002"
            iva = iva + float(impuesto.attrib["Importe"])#Si si se cumple la validación sumamos a la variable "iva" el "Importe" del xml convertido a numero con "float" (ya que en el xml viene con formato de texto)
        else:
            otros_impuestos = otros_impuestos + float(impuesto.attrib["Importe"])

    #Aqui revisamos las retenciones del iva
    ret_impuestos = raiz.findall("cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion",ns)#creamos la variable impuestos y le decimos a que etiquetas del xml se debe ir(unas etiquetas estan dentro de otras)
    retenciones = 0
    for retencion in ret_impuestos:#hacemos que recorra la informacion que esta dentro de las etiquetas que le pasamos, esto con un for
        if retencion.attrib["Impuesto"] == "002":#revisamos y validamos con un if que en la etiqueta "Retencion" exista un bloque "Impuesto" que su valor sea "002"
            retenciones = retenciones + float(retencion.attrib["Importe"])#Si si se cumple la validación sumamos a la variable "retenciones" el "Importe" del xml convertido a numero con "float" (ya que en el xml viene con formato de texto)

    #Creamos un diccionario con los codigos de los tipos de pago
    formas_pago = {"28":"Tarjeta de Débito", "04":"Tarjeta de crédito","01":"Efectivo","03":"Transferencia electrónica de fondos"}
    pago_captado = raiz.attrib.get("FormaPago","No especifica")

    return{
        "fecha": raiz.attrib["Fecha"],
        "subtotal": float(raiz.attrib["SubTotal"]),
        "formapago": formas_pago.get(pago_captado,pago_captado),
        "total":float(raiz.attrib["Total"]),
        "nombre":emisor.attrib["Nombre"],
        "rfc":emisor.attrib["Rfc"],
        "uuid":timbre.attrib["UUID"],
        "descripcion":texto_conceptos,
        "iva":iva,
        "descuento":float(raiz.attrib.get("Descuento","0")),
        "ret_iva":retenciones,
        "otros_impuestos":otros_impuestos
    }

#datos = lee_factura("factura.xml")#guardamos en la variable "datos" el diccionario anterior
#print(datos)
#print(datos["nombre"])
#print(datos["descripcion"])
#print(datos["iva"])
#print(datos["descuento"])
#print(datos["ret_iva"])
#print(datos["otros_impuestos"])          
#print(datos["formapago"])      

