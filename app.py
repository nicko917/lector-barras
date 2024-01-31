# Script principal de Flask
from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)

# Configura el ProxyFix para simular una conexión HTTPS en local
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        df = pd.read_csv(file)
        # Aquí puedes procesar el DataFrame como necesites
        # Por ejemplo, guardar en una base de datos o realizar cálculos
        return jsonify({"message": "Archivo recibido y procesado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5000, debug=True)
