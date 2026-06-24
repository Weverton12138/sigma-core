import streamlit as st
from rembg import remove
from PIL import Image
import io

# Configuração da Página Web
st.set_page_config(
    page_title="🔥 SIGMA ClearCut - Removedor de Fundo",
    page_icon="✂️",
    layout="centered"
)

# Estilização Visual Cyberpunk
st.markdown("""
    <style>
        .stApp { background-color: #0b0f19; color: #ecf0f1; }
        h1, h2 { font-family: 'Courier New', monospace !important; color: #38bdf8 !important; text-align: center; }
        .stButton>button { background-color: #38bdf8; color: #0b0f19; font-weight: bold; width: 100%; height: 50px; border-radius: 8px; }
        .stButton>button:hover { background-color: #0ea5e9; box-shadow: 0 0 15px #38bdf8; }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ SIGMA ClearCut")
st.subheader("Sem enrolação: jogue sua imagem e baixe sem o fundo instantaneamente.")
st.write("---")

# Campo de Upload da Imagem
uploaded_file = st.file_uploader("Arraste e solte uma imagem aqui (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📸 Original")
        st.image(image, use_container_width=True)
        
    with col2:
        st.markdown("### 🚀 Resultado")
        
        with st.spinner("Analisando pixels e removendo o fundo..."):
            try:
                input_bytes = uploaded_file.getvalue()
                output_bytes = remove(input_bytes)
                output_image = Image.open(io.BytesIO(output_bytes))
                
                st.image(output_image, use_container_width=True)
                
                st.download_button(
                    label="📥 BAIXAR IMAGEM TRANSPARENTE",
                    data=output_bytes,
                    file_name="sigma_clearcut.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error("Erro ao processar a imagem. Certifique-se de que o arquivo não está corrompido.")

st.write("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Ferramenta utilitária real de processamento local.</p>", unsafe_allow_html=True)
