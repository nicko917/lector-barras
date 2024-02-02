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

def actualizar_datos_producto(idx, nombre, descripcion):
    # Actualiza los datos en el estado de sesión para un producto específico
    st.session_state['productos'][idx]['Nombre'] = nombre
    st.session_state['productos'][idx]['Descripción'] = descripcion

def main():
    st.title('Lector de Códigos de Barras y Entrada de Datos')

    # Inicializar el estado de sesión si no existe
    if 'productos' not in st.session_state:
        st.session_state['productos'] = []

    captured_image = st.camera_input("Captura un código de barras usando tu cámara")

    if captured_image is not None:
        image = Image.open(captured_image)
        codigo = leer_codigo_de_barras(image)
        if codigo and not any(prod["SKU"] == codigo for prod in st.session_state['productos']):
            st.session_state['productos'].append({"SKU": codigo, "Nombre": "", "Descripción": "", "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            st.success(f"Código de Barras Detectado: {codigo}")
        elif codigo:
            st.error("Código de barras duplicado.")
        else:
            st.error("No se detectó un código de barras válido.")

    # Crear campos de entrada para cada producto
    for idx, producto in enumerate(st.session_state['productos']):
        with st.container():
            st.write(f"SKU: {producto['SKU']}")
            nombre = st.text_input("Nombre", value=producto['Nombre'], key=f"nombre_{idx}")
            descripcion = st.text_area("Descripción", value=producto['Descripción'], key=f"descripcion_{idx}")
            actualizar_datos_producto(idx, nombre, descripcion)

    # Botón para borrar el último producto leído
    if st.button("Borrar Último Producto Leído"):
        if st.session_state['productos']:
            st.session_state['productos'].pop()
            st.success("Último producto eliminado.")
        else:
            st.error("No hay productos para eliminar.")

    # Botón para exportar a CSV
    if st.button("Exportar a CSV"):
        df = pd.DataFrame(st.session_state['productos'])
        st.download_button(label="Descargar CSV", data=df.to_csv(index=False), mime="text/csv", file_name="productos.csv")

if __name__ == "__main__":
    main()
