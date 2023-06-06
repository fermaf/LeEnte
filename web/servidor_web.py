from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar', methods=['POST'])
def cargar():
    archivo = request.files['archivo']

    if archivo.filename == '':
        return render_template('error.html', mensaje=mensaje)  #PAGINA SIN FICHERO ES NULO

    nombre_archivo = archivo.filename
    ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
    archivo.save(ruta_archivo)

    # Aquí puedes incluir tu lógica de procesamiento del archivo
    # Por ejemplo, leer el archivo, realizar cálculos, etc.

    # Al finalizar el procesamiento, muestra un mensaje de "paz mundial"
    mensaje = "Paz mundial"

    return render_template('borrame2.html')
    #return redirect(url_for('procesar'))

@app.route('/procesar')
def procesar():
    return render_template('borrame2.html')

if __name__ == '__main__':
    app.run()
