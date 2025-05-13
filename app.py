import streamlit as st
import requests 
import base64
import json
from PIL import Image

"""
# Cognitive Environment

Aplicação para detectar face para emisão de documentos,
validando existência de face e neutralidade via análise de imagem.

Caso o rosto esteja dentro dos padrões, a imagem é enviada autorizada para 
confecção de documento.
"""

foto = st.camera_input("Tire uma foto do seu rosto.")
if foto:
    with st.spinner("Analisando imagem..."):
        bytes_image = foto.getvalue()
        base64_image = base64.b64encode(bytes_image).decode('utf-8')

        payload = {"image_base64": base64_image}
        endpoint = st.secrets["API-ENDPOINT"]
        response = requests.post(endpoint, json=payload)

        if response.status_code == 200:
            response_data = json.loads(response.text)

            imagem = Image.open(foto)
            largura, altura = imagem.size

            left = response_data["boundingBox"]["Left"] * largura
            top = response_data["boundingBox"]["Top"] * altura
            width = response_data["boundingBox"]["Width"] * largura
            height = response_data["boundingBox"]["Height"] * altura

            regiao_interesse = imagem.crop((left, top, left + width, top + height))

            st.image(regiao_interesse)
            st.success("Imagem aprovada para confecção de documento.")
        else:
            st.error(response.text)