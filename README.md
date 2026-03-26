# 📚 RAG Antigravity - Visualización de Fuentes con Gemini 2.0

Este repositorio contiene una aplicación de **RAG (Retrieval-Augmented Generation)** avanzada desarrollada con **Streamlit**, diseñada para consultar documentos PDF de manera inteligente. El sistema no solo responde preguntas, sino que extrae y visualiza la página exacta del documento original como evidencia.

## 🚀 Características Principales

* **Orquestación de IA:** Utiliza el SDK de **Google Gen AI** con el modelo `gemini-2.0-flash` para respuestas rápidas y precisas.
* **Vector Database:** Indexación y búsqueda semántica mediante **Pinecone**.
* **Embeddings de Última Generación:** Implementación de `text-embedding-004` (o `gemini-embedding-001`) para una representación vectorial de alta calidad.
* **Visualización de Fuentes:** Integración con **PyMuPDF (fitz)** para capturar y mostrar imágenes de las páginas citadas en la respuesta.
* **Interfaz Interactiva:** Dashboard profesional construido en **Streamlit**.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.14+
* **LLM:** Google Gemini 2.0 Flash
* **Vector DB:** Pinecone
* **Frontend:** Streamlit
* **Procesamiento de PDF:** PyMuPDF

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:
1.  Una **Google AI Studio API Key**.
2.  Una cuenta en **Pinecone** y un índice configurado (dimensión 768).
3.  Python instalado en tu sistema.

## ⚙️ Configuración e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/AngelTroncoso/RagConPinecone.git](https://github.com/AngelTroncoso/RagConPinecone.git)
   cd RagConPineconeCrear y activar entorno virtual:

    Bash
    python -m venv .venv
    .\.venv\Scripts\activate
    Instalar dependencias:
    
    Bash
    pip install -r requirements.txt
    Variables de Entorno:
    Crea un archivo .env en la raíz del proyecto con el siguiente formato (no incluyas este archivo en tus commits):
    
    Fragmento de código
    GOOGLE_API_KEY=tu_api_key_aqui
    PINECONE_API_KEY=tu_api_key_aqui
    PINECONE_INDEX_NAME=nombre_de_tu_indice
    🚀 Ejecución
    Para lanzar la aplicación localmente:
    
    Bash
    python -m streamlit run app.py

---

### 📁 Estructura del Proyecto
app.py: Código principal de la aplicación y lógica de Streamlit.

documentos/: Carpeta local para depositar los archivos PDF a indexar.

requirements.txt: Lista de librerías necesarias.

.gitignore: Configuración para excluir archivos sensibles (.env, .venv).

Desarrollado por Angel Troncoso - Commercial Engineer & Auditor.


---

### ¿Cómo agregarlo a GitHub?
Como ya tienes el repo conectado, solo tienes que hacer esto en tu terminal de VS Code:

1.  Crea el archivo: `code README.md` (pega el contenido y guarda).
2.  Sube los cambios:
    ```powershell
    git add README.md
    git commit -m "Docs: add professional README"
    git push origin main
    ```
---

## ✒️ Autor y Créditos Personales

Este proyecto es parte del ecosistema de soluciones inteligentes desarrolladas por **Ángel Troncoso**, enfocado en la intersección de la ingeniería comercial, la auditoría y la inteligencia artificial generativa.

### 👤 Perfil Profesional
* **Rol:** Ingeniero Comercial & Contador Auditor Certificado.
* **Especialización:** Machine Learning (U. de Chile), Business Intelligence y Orquestación de Agentes Multimodales.
* **Ubicación:** Santiago, Chile 🇨🇱
* **Enfoque:** Transformación digital con metodología **Lean Six Sigma** y compromiso con la **Sostenibilidad Digital (Green Tech)**.

### 🚀 Otros Proyectos Destacados
* **BioTwin AI:** Agente multimodal para el análisis de datos clínicos y simulación de patrones de salud (Gemini + MedGemma).
* **Sistema BORAM:** Plataforma integral de gestión de licitaciones médicas desplegada sobre Supabase.
* **GitLab AI Security:** Agente autónomo para escaneo y respuesta a vulnerabilidades de seguridad.

### 📬 Contacto y Colaboración
Si estás interesado en implementar flujos de trabajo de **"Vibe Coding"**, automatización de auditorías o sistemas RAG personalizados, hablemos:

* **LinkedIn:** [linkedin.com/in/tu-usuario](https://www.linkedin.com/in/tu-usuario)
* **GitHub:** [@AngelTroncoso](https://github.com/AngelTroncoso)
* **Email:** [angeltroncoso2019@outlook.es]

---
*Hecho con ❤️ y "Vibe Coding" desde Santiago.*
