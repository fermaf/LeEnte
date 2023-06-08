#Para procesar excel
import openpyxl
from openpyxl.styles import Font
import requests
import xml.etree.ElementTree as ET
import datetime
import buscaNormasBCN as BCN

#Para web con flask
from flask import Flask, render_template, request, redirect, url_for, Response
import os
from subprocess import Popen, PIPE
import re
import time
from queue import Queue
from flask import send_file



cola= Queue()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar', methods=['POST']) #carga y procesa archivo excel
def cargar():
    
    esMetaData=False #si es falso buscará la URL del XML de la norma full en vez de la URL que solo tienen metadadata de la norma en los servicios del BCN.CL
    
    archivo = request.files['archivo']
    cliente_ip = request.remote_addr
    if archivo.filename == '':
        return render_template('error.html')  
    print("nombre_archivo1: "+archivo.filename)
    nombre_archivo = cliente_ip + archivo.filename 
    print("nombre_archivo2: "+nombre_archivo)

    ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
    print("ruta_archivo1: "+ruta_archivo)
    archivo.save(ruta_archivo) #guarda archivo localmente
     
    archivo_excel = openpyxl.load_workbook(ruta_archivo)

 
    #BCN.recorre_filas_excel(archivo_excel,esMetaData,cliente_ip,nombre_archivo)
    try:
        nombre_archivo_procesado=BCN.recorre_filas_excel(archivo_excel,esMetaData,cliente_ip,nombre_archivo,cola)
    except  Exception as e:
        print(str(e))
        return render_template('error.html')  

    return render_template('download.html', archivo=nombre_archivo_procesado)
  

@app.route('/download')
def download_file():
    archivo = request.args.get('archivo')
    ruta_archivo = os.path.join(os.getcwd(), archivo)
    return send_file(ruta_archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
