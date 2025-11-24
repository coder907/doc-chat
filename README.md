# **🤖 DocChat**
✨ **AI-powered Multi-Agent RAG system for intelligent document querying with fact verification**  

---

## 💡Overview

**DocChat** is a **multi-agent Retrieval-Augmented Generation (RAG) system** designed to help users query **long, complex documents** with **accurate, fact-verified answers**. Unlike traditional chatbots like **ChatGPT or DeepSeek**, which **hallucinate responses and struggle with structured data**, DocChat **retrieves, verifies, and corrects** answers before delivering them.  

### 😎 Key Features
✅ **Multi-Agent System** – A **Research Agent** generates answers, while a **Verification Agent** fact-checks responses.  
✅ **Hybrid Retrieval** – Uses **BM25 and vector search** to find the most relevant content.  
✅ **Handles Multiple Documents** – Selects the most relevant document even when multiple files are uploaded.  
✅ **Scope Detection** – Prevents hallucinations by **rejecting irrelevant queries**.  
✅ **Fact Verification** – Ensures responses are accurate before presenting them to the user.  
✅ **Web Interface with Gradio** – Allowing seamless document upload and question-answering.  

---

## ☝️ How DocChat Works

### 1️⃣ Query Processing & Scope Analysis
- Users **upload documents** and **ask a question**.  
- DocChat **analyzes query relevance** and determines if the question is **within scope**.  
- If the query is **irrelevant**, DocChat **rejects it** instead of generating hallucinated responses.  

### 2️⃣ Multi-Agent Research & Retrieval
- **Docling** parses documents into a structured format (Markdown, JSON).  
- **LangChain & ChromaDB** handle **hybrid retrieval** (BM25 + vector embeddings).  
- Even when **multiple documents** are uploaded, **DocChat finds the most relevant sections** dynamically.  

### 3️⃣ Answer Generation & Verification
- **Research Agent** generates an answer using retrieved content.  
- **Verification Agent** cross-checks the response against the source document.  
- If **verification fails**, a **self-correction loop** re-runs retrieval and research.  

### 4️⃣ Response Finalization
- **If the answer passes verification**, it is displayed to the user.  
- **If the question is out of scope**, DocChat informs the user instead of hallucinating.  

---

## 🎯 Why Use DocChat Instead of ChatGPT or DeepSeek?

| Feature | ChatGPT / DeepSeek | DocChat |
|---------|-----------------|---------|
| Retrieves from uploaded documents | ❌ | ✅ |
| Handles multiple documents | ❌ | ✅ |
| Extracts structured data from PDFs | ❌ | ✅ |
| Prevents hallucinations | ❌ | ✅ |
| Fact-checks answers | ❌ | ✅ |
| Detects out-of-scope queries | ❌ | ✅ |

🚀 *DocChat is built for enterprise-grade document intelligence, research, and compliance workflows.* 

---

## 💻 System Requirements

The installation process and app usage have been tested on **Windows 11** with **Anaconda3 2024.10 (Python 3.12.7 64-bit)** distribution. Slight modifications may be required on other systems and/or Python distributions.

## ⚙️ Installation Guide 

### 1️⃣ Clone the Repository
```
git clone https://github.com/coder907/doc-chat doc-chat
cd doc-chat
```

### 2️⃣ Set Up and Activate Virtual Environment 
```
conda create --name doc-chat-env python=3.12.7
conda activate doc-chat-env
```

### 3️⃣ Install Dependencies  
```
pip install -r requirements.txt
```

### 4️⃣ Set Up API Keys
DocChat uses **Gemini 2.5 Flash** model and requires an **Google API Key** for processing. Create `.env` file in the `doc-chat` folder and provide you API key in the following format:
```
GOOGLE_API_KEY = <YOUR_GOOGLE_API_KEY>
```

### 5️⃣ Run the Application
```
python app.py
```
DocChat will be accessible at `http://localhost:7860`.

## 🖥️ Usage Guide  

1️⃣ **Upload** one or more documents or select one of the examples from the drop-down menu.

2️⃣ **Enter a question** related to the document.  

3️⃣ Hit **Submit** button – DocChat retrieves, analyzes, and verifies the response.  

4️⃣ **Review** the answer and verification report.

5️⃣ **If the question is out of scope**, DocChat will inform you instead of fabricating an answer.  

---

## Attribution and Modifications

### 🙏 Attribution

This project is based on the following work: **[https://github.com/HaileyTQuach/docchat-docling](https://github.com/HaileyTQuach/docchat-docling)**

This project is licensed under **[Non-Commercial License](LICENSE.md)**.

### 🛠️ Modifications

The following modifications have been made:
* **Upgraded packages** to the latest versions.
* Updated agents to use Google **Gemini 2.5 Flash** model.
* Added two **example documents**.
* A couple of **small user interface tweaks**, such as using TextAreas for results.
* Updated **README.md**.

