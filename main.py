from fastapi import FastAPI,UploadFile,Form,File
from fastapi.responses import FileResponse
from llenar_excel import llenar_excel


app = FastAPI()

@app.get("/")
def inicio ():
    return{"mensaje":"Hola,comprobaciones"}

@app.post("/generar")
def generar (archivos: list[UploadFile] = File(), trabajador: str = Form(), obra: str = Form()):

    archivo = []#Creamos una lista vacia para mandar lo que atrape el for 
    for documento in archivos:#Generamos el for para que busque dentro de los archivos subidos por el usuario 
        archivo.append(documento.file)#Con .append añadimos a la lista los objetos tipo archivo encontrados con el .file
    ruta = llenar_excel(archivo,trabajador,obra)#Mandamos llamar la función "llenar_excel" y le pasamos los datos (archivo,trabajador,obra), la guardo en una variable "ruta", para poder pasarla al return




    return FileResponse(ruta, filename="Comprobacion.xlsx")



