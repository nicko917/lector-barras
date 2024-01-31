import streamlit as st
import pandas as pd
from PIL import Image
from pyzbar.pyzbar import decode
import datetime

def leer_codigo_de_barras(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")  # Decodificar a texto
    return None

def main():
    st.title('Lector de Códigos de Barras')

    # Lista para almacenar los códigos de barras y la fecha de escaneo
    codigos_de_barras = []

    # Uso de st.camera_input para capturar la imagen
    captured_image = st.camera_input("Captura un código de barras usando tu cámara")

    if captured_image is not None:
        # Procesa la imagen capturada
        image = Image.open(captured_image)
        codigo = leer_codigo_de_barras(image)
        if codigo:
            codigos_de_barras.append({"Código": codigo, "Fecha": datetime.datetime.now()})
            st.success(f"Código de Barras Detectado: {codigo}")
        else:
            st.error("No se detectó un código de barras válido.")

    # Mostrar los códigos de barras almacenados
    if codigos_de_barras:
        st.write("Códigos de Barras Escaneados:")
        for item in codigos_de_barras:
            st.write(f"Código: {item['Código']}, Fecha: {item['Fecha']}")

    # Botón para exportar a CSV
    if st.button("Exportar a CSV"):
        df = pd.DataFrame(codigos_de_barras)
        st.download_button(label="Descargar CSV", data=df.to_csv(index=False), file_name="codigos_de_barras.csv", mime="text/csv")

if __name__ == "__main__":
    main()
