# **RAG Chatbot - README**

## **Overview**
This project implements a **Retrieval-Augmented Generation (RAG) chatbot** using:
- **Streamlit** for the UI
- **Google Generative AI** for embeddings and response generation
- **Qdrant** for vector search
- **PyPDF2, pdf2image, pytesseract** for text and image extraction from PDFs
- **LangGraph** for chatbot workflow execution

The chatbot enables users to upload PDFs, extract and store text embeddings, and ask questions based on the document content.

---

## **RAID Matrix**

### **Risks**

| **ID** | **Risk** | **Mitigation/Action Plan** |
|--------|---------|-----------------------------|
| **R1** | Data Security Risk: User credentials stored in JSON are not secure. | Implement **hashed passwords** (bcrypt) and consider **OAuth authentication**. |
| **R2** | Qdrant Downtime: If Qdrant is down, document retrieval will fail. | Implement a **backup vector store** (e.g., FAISS) or a fallback mechanism. |
| **R3** | Slow Response Time: Large PDFs can cause delays. | Optimize chunking strategy and cache embeddings for frequent queries. |
| **A1** | Users upload clear, readable PDFs. | Provide error handling for invalid PDFs and notify users about poor-quality images. |
| **A2** | Internet availability is required for embeddings and API calls. | Implement **offline mode** with local models (e.g., Hugging Face transformers). |
| **I1** | Incorrect retrieval: Retrieved documents may not be contextually relevant. | Improve **vector search ranking** with metadata-based filtering. |
| **I2** | UI Freezing: Streamlit may become unresponsive with large PDFs. | Implement **progress indicators** and process PDFs asynchronously. |
| **I3** | Authentication Bypass: JSON-based authentication is insecure. | Use **hashed passwords** and consider database-backed authentication. |
| **D1** | Google Generative AI: Used for embeddings and responses. | Ensure alternative APIs (e.g., OpenAI, Hugging Face) are available. |
| **D2** | Qdrant Vector Store: Required for document retrieval. | Implement a **backup vector store** (FAISS, Weaviate). |
| **D3** | PyPDF2 & pdf2image: Used for text/image extraction. | Add support for **alternative libraries** (e.g., pdfplumber). |

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/RAG-chatbot.git
   cd RAG-chatbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the chatbot:
   ```bash
   streamlit run trial.py
   ```

---

## **Usage**
- Upload a PDF document.
- Ask questions related to the document.
- The chatbot will retrieve relevant information using **Qdrant** and **Google Generative AI**.

---

## **Contributing**
- Fork the repository.
- Create a new branch (`feature-new-feature`).
- Commit your changes.
- Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

