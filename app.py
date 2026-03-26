import os
import streamlit as st
import fitz  # PyMuPDF
from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai
from google.genai import types

# Cargar variables de entorno
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
CORPUS_PATH = os.getenv("CORPUS_PATH", "./documentos")

# Configurar página
st.set_page_config(page_title="RAG Interactiva", layout="wide", page_icon="📚")

# Inicializar clientes
@st.cache_resource
def init_clients():
    if not GOOGLE_API_KEY or not PINECONE_API_KEY:
        st.error("Faltan las credenciales en el archivo .env")
        st.stop()
    pc = Pinecone(api_key=PINECONE_API_KEY)
    ai_client = genai.Client(api_key=GOOGLE_API_KEY)
    return pc, ai_client

pc, ai_client = init_clients()

@st.cache_resource
def get_pinecone_index():
    return pc.Index(PINECONE_INDEX_NAME)

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    # Modelo correcto disponible en tu cuenta: gemini-embedding-001
    # output_dimensionality=768 para coincidir con tu índice de Pinecone
    response = ai_client.models.embed_content(
        model='gemini-embedding-001', 
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768
        )
    )
    return response.embeddings[0].values
    
    
def process_documents(folder_path):
    index = get_pinecone_index()
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    docs = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    if not docs:
        st.warning(f"No hay PDFs en la carpeta: {folder_path}")
        return

    vectors = []
    vector_id = 0
    
    progress_bar = st.progress(0, text="Procesando documentos...")
    total_docs = len(docs)
    
    for i, doc_name in enumerate(docs):
        doc_path = os.path.join(folder_path, doc_name)
        pdf_doc = fitz.open(doc_path)
        
        for page_num in range(len(pdf_doc)):
            page = pdf_doc.load_page(page_num)
            text = page.get_text()
            
            if text.strip():
                emb = get_embedding(text)
                vectors.append({
                    "id": f"{doc_name}_p{page_num}_{vector_id}",
                    "values": emb,
                    "metadata": {
                        "source": doc_path,
                        "page": page_num,
                        "text": text
                    }
                })
                vector_id += 1
                
                # Subir por lotes para no saturar Pinecone
                if len(vectors) >= 50:
                    index.upsert(vectors=vectors)
                    vectors = []
                    
        progress_bar.progress((i + 1) / total_docs, text=f"Procesando {doc_name}...")
                    
    if vectors:
        index.upsert(vectors=vectors)
        
    st.success("¡Corpus indexado correctamente en Pinecone!")

def render_page_image(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    # Generar captura de la página
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Zoom x2 para mayor resolución
    return pix.tobytes("png")

st.title("📚 RAG con Visualización de Fuentes (Gemini 2.0)")

# Sidebar para cargar documentos
with st.sidebar:
    st.header("🗂️ Tu Corpus")
    st.markdown("Deja tus archivos PDF en la carpeta que configuraste (`./documentos` por defecto) y haz clic en actualizar.")
    
    if st.button("Indexar/Actualizar carpeta"):
        with st.spinner("Indexando..."):
            process_documents(CORPUS_PATH)

# Estado del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            cols = st.columns(len(message["sources"]))
            for idx, source in enumerate(message["sources"]):
                with cols[idx]:
                    st.image(source["image"], caption=f"📄 {os.path.basename(source['doc'])} - Pág {source['page']}")

# Input de usuario
if prompt := st.chat_input("Hazme una pregunta sobre tus documentos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando Pinecone y Gemini..."):
            # 1. Crear vector de búsqueda
            query_emb = get_embedding(prompt, task_type="RETRIEVAL_QUERY")
            
            # 2. Buscar similitudes
            index = get_pinecone_index()
            results = index.query(vector=query_emb, top_k=3, include_metadata=True)
            
            if not results.matches:
                fallback = "No encontré referencias en el corpus."
                st.markdown(fallback)
                st.session_state.messages.append({"role": "assistant", "content": fallback})
            else:
                # 3. Preparar contexto y extraer capturas de imagen (fuentes originales)
                context = ""
                sources_data = []
                
                for idx, match in enumerate(results.matches):
                    meta = match.metadata
                    context += f"--- FUENTE {idx + 1} ({os.path.basename(meta['source'])}, Página {int(meta['page']) + 1}) ---\n{meta['text']}\n"
                    
                    # Generar captura de esa página original
                    try:
                        img_bytes = render_page_image(meta['source'], int(meta['page']))
                        sources_data.append({
                            "doc": meta['source'],
                            "page": int(meta['page']) + 1,
                            "image": img_bytes
                        })
                    except Exception as e:
                        print(f"Error al generar imagen de la fuente: {e}")
                
                # 4. Generar respuesta final con Gemini
                sys_prompt = f"Usa el siguiente contexto para responder a la pregunta. Cita siempre la fuente y página usada.\n\nCONTEXTO:\n{context}\n\nPREGUNTA:\n{prompt}"
                
                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash', # o gemini-2.5-pro
                    contents=sys_prompt
                )
                
                st.markdown(response.text)
                
                # 5. Desplegar imágenes (evidencias del manual/pdf) debajo de la respuesta
                if sources_data:
                    st.markdown("#### Fuentes originales consultadas:")
                    cols = st.columns(len(sources_data))
                    for idx, src in enumerate(sources_data):
                        with cols[idx]:
                            st.image(src["image"], caption=f"📄 {os.path.basename(src['doc'])} - Pág {src['page']}")
                
                # Guardar en memoria
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text,
                    "sources": sources_data
                })
