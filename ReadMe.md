### **Progetto: "CV-AI-Screener" - Sistema Intelligente di Analisi e Screening dei Curriculum**

**Obiettivo:** Automatizzare la raccolta, l'analisi e il ranking dei CV da una mailbox di recruiting, integrando intelligentemente un LLM per una valutazione contestuale basata sulla job description.

**Tecnologie Impiegate:**
*   **Python** (Lingua franca)
*   **Selenium** (Automazione del browser per scaricare i CV)
*   **Cucumber** (BDD per definire i criteri di business in linguaggio naturale)
*   **LangChain & RAG** (Orchestrare il processo con l'LLM e fornirgli il contesto)
*   **Prompt Engineering** (Progettare prompt efficaci per l'analisi)
*   **API REST** (Modulo FastAPI per interrogare il sistema)
*   **LLM** (OpenAI GPT-4-turbo o un modello locale come Llama 3 via Ollama)

### **Fase 1: Setup e Installazione (Passo 0)**

**Creazione di un ambiente virtuale e installa le dipendenze:**
```bash
mkdir cv-ai-screener && cd cv-ai-screener
python -m venv venv
source venv/bin/activate  # Su Windows: .\venv\Scripts\activate

# Installazione pacchetti core
pip install langchain langchain-openai langchain-community selenium beautifulsoup4 python-dotenv
# Per il processing dei PDF
pip install pypdf unstructured
# Per le API
pip install "fastapi[standard]" uvicorn
# Per i test BDD
pip install behave cucumber-tag-expressions
# Database vettoriale (leggero)
pip install chromadb


**3. Configurare le variabili d'ambiente (`.env`):**
```ini
OPENAI_API_KEY="your-openai-api-key-here"
EMAIL_ADDRESS="your-recruiter-email"
EMAIL_PASSWORD="your-app-password" # Usa una password specifica per app!
LANGCHAIN_TRACING_V2=false