import streamlit as st
import pandas as pd
from PIL import Image
from pyzbar.pyzbar import decode
import datetime
import base64

def leer_codigo_de_barras(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")  # Decodificar a texto
    return None

def main():
    st.title('Lector de Códigos de Barras y Entrada de Datos')

    if 'productos' not in st.session_state:
        st.session_state['productos'] = []

    captured_image = st.camera_input("Captura un código de barras usando tu cámara")

    if captured_image is not None:
        image = Image.open(captured_image)
        codigo = leer_codigo_de_barras(image)
        if codigo and not any(prod["SKU"] == codigo for prod in st.session_state['productos']):
            st.session_state['productos'].append({
                "SKU": codigo, 
                "Nombre": "", 
                "Descripción corta": "", 
                "Inventario": "", 
                "editar": True,
                "guardado": False
            })
            st.success(f"Código de Barras Detectado: {codigo}")
        elif codigo:
            st.error("Código de barras duplicado.")
        else:
            st.error("No se detectó un código de barras válido.")

    for idx, producto in enumerate(st.session_state['productos']):
        with st.container():
            if producto['editar']:
                st.write(f"SKU: {producto['SKU']}")
                producto['Nombre'] = st.text_input("Nombre", value=producto['Nombre'], key=f"nombre_{idx}")
                producto['Descripción corta'] = st.text_area("Descripción corta", value=producto['Descripción corta'], key=f"descripcion_corta_{idx}")
                producto['Inventario'] = st.text_input("Inventario", value=producto['Inventario'], key=f"inventario_{idx}")
                if st.button("Guardar", key=f"guardar_{idx}"):
                    producto["guardado"] = True
                    producto["editar"] = False
            elif producto["guardado"]:
                st.write(f"SKU: {producto['SKU']} - Información guardada.")
                if st.button("🖉 Editar", key=f"editar_{idx}"):
                    producto["editar"] = True
                    producto["guardado"] = False

    if st.button("Borrar Último Producto Leído"):
        if st.session_state['productos']:
            st.session_state['productos'].pop()
            st.success("Último producto eliminado.")
        else:
            st.error("No hay productos para eliminar.")

    if st.button("Exportar a CSV"):
        columnas = [
            "ID", "Tipo", "SKU", "Nombre", "Publicado", "¿Está destacado?", 
            "Visibilidad en el catálogo", "Descripción corta", "Descripción", 
            "Día en que empieza el precio rebajado", "Día en que termina el precio rebajado", 
            "Estado del impuesto", "Clase de impuesto", "¿Existencias?", "Inventario", 
            "Cantidad de bajo inventario", "¿Permitir reservas de productos agotados?", 
            "¿Vendido individualmente?", "Peso (kg)", "Longitud (cm)", "Anchura (cm)", 
            "Altura (cm)", "¿Permitir valoraciones de clientes?", "Nota de compra", 
            "Precio rebajado", "Precio normal", "Categorías", "Etiquetas", "Clase de envío", 
            "Imágenes", "Límite de descargas", "Días de caducidad de la descarga", 
            "Superior", "Productos agrupados", "Ventas dirigidas", "Ventas cruzadas", 
            "URL externa", "Texto del botón", "Posición", "EAN"
        ]
        df_export = pd.DataFrame(columns=columnas)
        rows_list = []
        for producto in st.session_state['productos']:
            row = {
                "SKU": producto["SKU"], 
                "Nombre": producto["Nombre"], 
                "Descripción corta": producto["Descripción corta"], 
                "Inventario": producto["Inventario"]
                # Puedes agregar valores predeterminados para otras columnas si es necesario
            }
            rows_list.append(row)
        
        df_export = pd.concat([df_export, pd.DataFrame(rows_list)], ignore_index=True)
        
          # Usar st.download_button para descargar el CSV
        csv = df_export.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="productos.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
