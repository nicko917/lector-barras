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

    # Inicializa el estado de sesión si no existe
    if 'codigos_de_barras' not in st.session_state:
        st.session_state['codigos_de_barras'] = []

    # Uso de st.camera_input para capturar la imagen
    captured_image = st.camera_input("Captura un código de barras usando tu cámara")

    if captured_image is not None:
        image = Image.open(captured_image)
        codigo = leer_codigo_de_barras(image)
        if codigo:
            st.session_state['codigos_de_barras'].append({"Código": codigo, "Fecha": datetime.datetime.now()})
            st.success(f"Código de Barras Detectado: {codigo}")
        else:
            st.error("No se detectó un código de barras válido.")

    # Botón para borrar el último código de barras leído
    if st.button("Borrar Último Código Leído"):
        if st.session_state['codigos_de_barras']:
            st.session_state['codigos_de_barras'].pop()
            st.success("Último código de barras eliminado.")
        else:
            st.error("No hay códigos de barras para eliminar.")

    # Mostrar los códigos de barras almacenados
    if st.session_state['codigos_de_barras']:
        st.write("Códigos de Barras Escaneados:")
        for item in st.session_state['codigos_de_barras']:
            st.write(f"Código: {item['Código']}, Fecha: {item['Fecha']}")

    # Botón para exportar a CSV
    if st.button("Exportar a CSV"):
        df = pd.DataFrame(st.session_state['codigos_de_barras'])
        st.download_button(label="Descargar CSV", data=df.to_csv(index=False), file_name="codigos_de_barras.csv", mime="text/csv")

if __name__ == "__main__":
    main()
