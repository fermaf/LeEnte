# Web service de Ley Chile para desarrolladores
# https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service
#

import openpyxl
from openpyxl.styles import Font

import requests
#from bs4 import BeautifulSoup
#import json
import time
import random
import xml.etree.ElementTree as ET
import datetime


def visualizar_estructura(elemento, indent=""):
    # Obtener el nombre del elemento
    nombre = elemento.tag
    
    # Imprimir el nombre del elemento
    print(indent + nombre)
    
    # Recorrer los subelementos recursivamente
    for subelemento in elemento:
        visualizar_estructura(subelemento, indent + "  ")

def mostrar_estructura(elemento, nivel=0):
    # Mostrar nombre del elemento y atributos
    print(' ' * nivel + f"-(a) {elemento.tag}")
    for atributo, valor in elemento.attrib.items():
        print(' ' * nivel + f"  -(b) {atributo}: {valor}")

    # Recorrer los subelementos recursivamente
    for subelemento in elemento:
        mostrar_estructura(subelemento, nivel + 2)


# Cargar el archivo de Excel
archivo_excel = openpyxl.load_workbook('marco_normativo.xlsx')
#hoja_excel=sheet = workbook['chao']
hoja_excel = archivo_excel.active
ultima_columna=hoja_excel.max_column


# Recorrer las filas de la hoja de Excel
for indice, fila in enumerate(hoja_excel.iter_rows(min_row=3, min_col=8, max_col=8, values_only=True), start=3):
    # Obtener la dirección web que está en la columna F
    url = fila[0]
    #print("URL= ",url)
    if url is not None and (url.find("bcn.cl") != -1 or url.find("leychile.cl") != -1):
             # Obtener el id de la norma desde la URL
            id_norma = None
            if "idNorma=" in url:
                id_norma = url.split("idNorma=")[1].split("&")[0]

            if id_norma is not None:

                # Construir la URL para obtener los datos de la norma en base a un XML de la norma completa (Última versión de cualquier norma (leyes, decretos, tratados, DL, DFL, resoluciones, etc.))
                # https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service
                #url2 = f"https://servicios-leychile.bcn.cl/Consulta/obtxml?opt=7&idNorma={id_norma}"
                #url2=f"https://www.leychile.cl/Consulta/obtxml?opt=4546&idNorma=1146551" #URL DE EJEMPLO (para debug)
                

                #URL SOLO DE METDATA de la NOrma
                url2 = f"https://www.leychile.cl/Consulta/obtxml?opt=4546&idNorma={id_norma}"
                #url2 = f"https://www.leychile.cl/Consulta/obtxml?opt=4546&idNorma=1146551"
                time.sleep(random.uniform(0.1, 0.5))
                headers = { 
                            "accept": "application/xml"
                        }
                #print("url2 :",url2,"\n\n\n")
                respuesta = requests.get(url2, headers=headers)
                xml_data = respuesta.content
                arbol = ET.ElementTree(ET.fromstring(xml_data))
                raiz = arbol.getroot()
                
                """ 
                #INCIO Sección para resctar campos asumiendo que el XML es de la norma completa (f"https://servicios-leychile.bcn.cl/Consulta/obtxml?opt=7&idNorma={id_norma}")
                #Última versión de cualquier norma (leyes, decretos, tratados, DL, DFL, resoluciones, etc.)
                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Identificador') #Promulgacion -- Publicacion
                fechas_norma = tmp.attrib
                
                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Tipo') #Tipo Norma
                tipo_norma = tmp.text


                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Numero') #Numero norma
                numero_norma = tmp.text 

                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}TituloNorma') #Titulo Norma
                titulo_norma = tmp.text 

                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Norma') #Vigencia norma
                norma_derogada=raiz.attrib.get("derogado")
                nombre2 = raiz.find('Identificador')

                print("Norma Orgánica,",tipo_norma,"|",numero_norma,"|",titulo_norma,"|",datetime.datetime.strptime(fechas_norma.get("fechaPublicacion"), "%Y-%m-%d").strftime("%d/%m/%Y"),"|",url,",", datetime.datetime.strptime(fechas_norma.get("fechaPromulgacion"), "%Y-%m-%d").strftime("%d/%m/%Y"))
                #FIN de Sección para resctar campos asumiendo que el XML es de la norma completa 
                """
                
                #
                #INCIO Sección para resctar campos asumiendo que el XML es de la norma Consulta por los metadatos de una norma (Última versión de cualquier norma (leyes, decretos, tratados, DL, DFL, resoluciones, etc.))
                # Este es la URL genrica  (f"https://servicios-leychile.bcn.cl/Consulta/obtxml?opt=7&idNorma={id_norma}")
                #
                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Identificador') #Fecha Publicacion
                fecha_publicacion = tmp.attrib.get("fechaPublicacion")
                fecha_publicacion = datetime.datetime.strptime(fecha_publicacion, "%Y-%m-%d").strftime("%d/%m/%Y") #Formatea a DD/MM/YYYY

                #fecha_promulgacion=tmp.attrib.get("fechaPromulgacion")
                #fecha_promulgacion=datetime.datetime.strptime(fecha_promulgacion, "%Y-%m-%d").strftime("%d/%m/%Y") #Formatea a DD/MM/YYYY
                
                caracteres_a_eliminar = ['\n', '\r', '\b', '\t']
                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Encabezado') #Fecha ultima versión y su vigencia
                ultima_version=tmp.attrib.get("fechaVersion")
                ultima_version = datetime.datetime.strptime(ultima_version, "%Y-%m-%d").strftime("%d/%m/%Y") #Formatea a DD/MM/YYYY
                vigencia=tmp.attrib.get("derogado")

  
                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Tipo') #Tipo Norma
                tipo_norma = tmp.text.strip()
                for caracter in caracteres_a_eliminar:
                    tipo_norma = tipo_norma.replace(caracter, '')
                
            

                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Numero') #Numero norma
                numero_norma = tmp.text.strip()
                for caracter in caracteres_a_eliminar:
                    numero_norma = numero_norma.replace(caracter, '')
                #if "EXENTA" in numero_norma:
                #    tipo_norma = tipo_norma.title() + " Exenta"  #agraga la palabra exenta a tipo de norma que es una "Resolución o Decreto"
                #    numero_norma = "".join(filter(str.isdigit, numero_norma)) #deja el numero de norma solo en digitos, eliminando la palabra "EXENTA"
                solo_digitos = ""
                sin_digitos = ""
                for caracter in numero_norma:
                    if caracter.isdigit():
                        solo_digitos += caracter
                    else:
                        sin_digitos += caracter
                tipo_norma = tipo_norma.title() + sin_digitos.title()  #agraga la palabra EXENTA o EXENTO al tipo de norma que puede ser  "Resolución o Decreto"
                numero_norma=solo_digitos





                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}TituloNorma') #Titulo Norma
                titulo_norma = tmp.text.strip()
                for caracter in caracteres_a_eliminar:
                    titulo_norma = titulo_norma.replace(caracter, '')
                #
                #print("HOLA: ",titulo_norma,"\n")
                #print("\n",xml_data,"\n")
            




                tmp = raiz.find('.//{http://www.leychile.cl/esquemas}Organismo') #Nombre del Organizmo
                organismo = tmp.text.strip()
                for caracter in caracteres_a_eliminar:
                    organismo = organismo.replace(caracter, '')


                norma_derogada=raiz.attrib.get("derogado")
                nombre2 = raiz.find('Identificador')

                print(organismo,"|",tipo_norma,"|",numero_norma,"|",titulo_norma,"|",fecha_publicacion,"|",ultima_version,"|",url,"|",vigencia)

                siguiente_columna=ultima_columna + 1
                hoja_excel.cell(row=indice, column=siguiente_columna, value=organismo)
                siguiente_columna +=1

                hoja_excel.cell(row=indice, column=siguiente_columna, value=tipo_norma)
                siguiente_columna +=1

                hoja_excel.cell(row=indice, column=siguiente_columna, value=numero_norma)
                siguiente_columna +=1

                hoja_excel.cell(row=indice, column=siguiente_columna, value=titulo_norma)
                siguiente_columna +=1

                hoja_excel.cell(row=indice, column=siguiente_columna, value=fecha_publicacion)
                siguiente_columna +=1

                hoja_excel.cell(row=indice, column=siguiente_columna, value=ultima_version)
                siguiente_columna +=1
                
                hoja_excel.cell(row=indice, column=siguiente_columna, value=url)
                siguiente_columna +=1


                if "no derogado" not in vigencia:
                    hoja_excel.cell(row=indice, column=siguiente_columna).font = Font(color="FF0000")  # cambia color rojo si es distinto a "no derogado"
                hoja_excel.cell(row=indice, column=siguiente_columna, value=vigencia)
           
                siguiente_columna =ultima_columna #Como es el final del ciclo se re inicia la poscion
                
                #
                #
                #FIN de Sección para resctar campos asumiendo que el XML es de la norma es solo metadata
                #
                #
                
archivo_excel.save(filename='marco_normativo.xlsx')




      
"""# Escribir los resultados en la hoja de Excel
for row, result in zip(sheet.iter_rows(min_row=2, min_col=1, max_col=6), results):
    row[4].value = result[0]
    row[6].value = result[1]
    row[7].value = result[2]

# Guardar los cambios en el archivo de Excel
workbook.save('archivo_excel_con_resultados.xlsx')

"""