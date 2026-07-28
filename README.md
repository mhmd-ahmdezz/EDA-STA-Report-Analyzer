# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Mohamed Ahmed Ezz-edin Hussien       |
| Project Name     | EDA STA Report Analyzer              |
| GitHub Username  | mhmd-ahmdezz                         |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en) |

---

# 📖 Project Overview

Digging through a synthesis timing report to find and understand a violation is slow and repetitive — engineers scroll through hundreds of `Startpoint → Endpoint` blocks by hand to spot the worst offenders and reason about their root cause.

**EDA STA Report Analyzer** is a Retrieval-Augmented Generation (RAG) assistant that ingests Static Timing Analysis (STA) `.rpt` files and lets you ask natural-language questions about them — e.g. *"What's causing the worst timing violation?"* or *"Summarize all violated paths in module X"* — and get back a structured, engineer-style diagnosis with concrete fix recommendations.

---

# ✨ Features

* **Custom `.rpt` parser** — splits a raw synthesis timing report into individual timing-path blocks and extracts structured metadata: slack status (`VIOLATED` / `MET`), slack value, startpoint, endpoint, path group, path type, module, and the top delay-contributing cells.
* **Semantic search over timing paths** — each parsed path is embedded with a Hugging Face sentence-transformer model and indexed in a FAISS vector store.
* **Metadata-filtered retrieval** — a self-query retriever lets questions be filtered by slack status, module, startpoint/endpoint, or path group (with a graceful fallback to plain similarity search if self-query isn't available).
* **LLM-generated root-cause diagnosis** — a system prompt frames the LLM as a senior ASIC/STA engineer, returning a structured answer: path summary → root-cause diagnosis (cell-delay vs. interconnect-dominated) → prioritized fixes (RTL restructuring → pipeline insertion → cell sizing / Vt swap → constraint relaxation as a last resort).
* **Streamlit chat UI** — upload a report, see live summary metrics (total paths, violation count, Worst Negative Slack), and chat with the copilot about the results.

---

# 🛠️ Technologies Used

- **Language:** Python
- **RAG / Orchestration:** LangChain (`langchain-core`, `langchain-community`, `langchain-huggingface`)
- **Embeddings:** Hugging Face `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store:** FAISS
- **LLM:** Groq API — Llama 3.1 8B Instant (`langchain-groq`)
- **Backend API:** FastAPI + Uvicorn
- **Tunneling:** ngrok (`pyngrok`) — exposes the Kaggle-hosted backend to the local frontend
- **Frontend:** Streamlit
- **Notebook environment:** Kaggle

---

# 🏗️ Architecture

The project runs as two connected pieces:

1. **Backend (Kaggle notebook + FastAPI + ngrok):** the notebook installs dependencies, defines the parser / vector store / retriever / LLM chain, starts a FastAPI server with `/upload` and `/query` endpoints, and opens an ngrok tunnel so it's reachable from outside Kaggle.
2. **Frontend (`app.py`, Streamlit):** runs locally. You paste in the ngrok URL and your own Groq API key, upload a `.rpt` file (sent to `/upload` to be parsed and indexed), and then chat with the report (each question is sent to `/query`, which runs the LangChain RAG chain and returns a diagnosis).

```
Streamlit (local)  --ngrok tunnel-->  FastAPI (Kaggle)  -->  LangChain RAG chain
     |                                                              |
     |-- upload .rpt ---------------------------------------------->|
     |                                          parse -> embed -> FAISS index
     |-- ask question -------------------------------------------->|
     |                                     retrieve paths -> Groq (Llama 3.1) -> answer
     |<-- diagnosis + fix recommendations --------------------------|
```

---

# ⚙️ Installation

**1. Backend (Kaggle)**
- Open the notebook on Kaggle and run all cells.
- Set your Groq API key as a Kaggle secret / environment variable (**do not hardcode it in the notebook**).
- Copy the ngrok URL printed at the end of the run.

**2. Frontend (local)**
```bash
pip install streamlit requests
streamlit run app.py
```
- In the sidebar, paste the ngrok URL from the backend and your own Groq API key.

---

# 🚀 Usage

1. Start the Kaggle backend and copy its ngrok URL.
2. Launch the Streamlit app and enter the URL + your Groq key in the sidebar.
3. Upload a synthesis timing report (`.rpt`, `.txt`, or `.log`) and click **"Process & Index Report"**.
4. Review the summary metrics (total paths, violations, Worst Negative Slack).
5. Ask questions in the chat, for example:
   - *"What is causing the worst timing violation?"*
   - *"Summarize all violated paths in module X."*
   - *"Is this path cell-delay or interconnect-dominated?"*

---

# 📸 Demo



---

# 📈 Results


---

# 🔮 Future Improvements

* Persist the vector store across sessions instead of rebuilding it per upload
* Support additional report formats (e.g. Yosys or PrimeTime output, not just Design Compiler)
* Auto-generate suggested RTL/constraint diffs alongside the text recommendations
* Replace the Kaggle + ngrok backend with a permanently hosted service

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.