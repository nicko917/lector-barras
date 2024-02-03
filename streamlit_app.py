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

def guardar_datos(idx):
    # Actualiza el estado para indicar que los datos se han guardado
    st.session_state['productos'][idx]['editar'] = False

def editar_datos(idx):
    # Actualiza el estado para indicar que los datos están siendo editados
    st.session_state['productos'][idx]['editar'] = True

def main():
    st.title('Lector de Códigos de Barras y Entrada de Datos')

    if 'productos' not in st.session_state:
        st.session_state['productos'] = []

    captured_image = st.camera_input("Captura un código de barras usando tu cámara")

    if captured_image is not None:
        image = Image.open(captured_image)
        codigo = leer_codigo_de_barras(image)
        if codigo and not any(prod["SKU"] == codigo for prod in st.session_state['productos']):
            st.session_state['productos'].append({"SKU": codigo, "Nombre": "", "Descripción": "", "editar": True})
            st.success(f"Código de Barras Detectado: {codigo}")
        elif codigo:
            st.error("Código de barras duplicado.")
        else:
            st.error("No se detectó un código de barras válido.")

    for idx, producto in enumerate(st.session_state['productos']):
        with st.container():
            st.write(f"SKU: {producto['SKU']}")
            if producto['editar']:
                producto['Nombre'] = st.text_input("Nombre", value=producto['Nombre'], key=f"nombre_{idx}")
                producto['Descripción'] = st.text_area("Descripción", value=producto['Descripción'], key=f"descripcion_{idx}")
                guardar_button = st.button("Guardar", key=f"guardar_{idx}", on_click=guardar_datos, args=(idx,))
            else:
                editar_button = st.button("🖉 Editar", key=f"editar_{idx}", on_click=editar_datos, args=(idx,))

    if st.button("Borrar Último Producto Leído"):
        if st.session_state['productos']:
            st.session_state['productos'].pop()
            st.success("Último producto eliminado.")
        else:
            st.error("No hay productos para eliminar.")

    if st.button("Exportar a CSV"):
        df = pd.DataFrame(st.session_state['productos'])
        st.download_button(label="Descargar CSV", data=df.to_csv(index=False), mime="text/csv", file_name="productos.csv")

if __name__ == "__main__":
    main()


