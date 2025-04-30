# 📄 Chat with your PDFs (100% Local)

A fully local chatbot powered by Ollama (LLaMA 3) that lets you interact with the content of your PDF files using natural language — no internet or OpenAI key needed.

Made by **Satya** (@programmingxpert) 
With ❤️

---

## 🚀 Features

- Chat with multiple PDFs at once
- 100% local processing — nothing leaves your machine
- LLaMA 3 + sentence-transformer embeddings
- Friendly chat interface with real-time "Thinking..." feedback
- No reuploading needed — just press 🔄 Refresh to re-index new PDFs
- Smart enough to answer meta-questions (e.g. "how many PDFs are loaded?", "what are you?")



## 📦 Requirements

- Python 3.10 or 3.11  
- [Ollama](https://ollama.com) installed and running (`ollama run llama3` at least once)

---

## 🛠️ Setup Instructions

1. **Install Python dependencies**  
   Open a terminal and run:
   ```bash
   pip install -r requirements.txt
2. **Make sure Ollama is running**
Open another terminal and run:

```bash
ollama run llama3
```
3. **Add your PDFs**
Place all your .pdf files into the pdfs/ folder.

4. **Run the app**
In the terminal, run:
```bash
streamlit run app.py
```
5. **Use the app**

- Visit http://localhost:8501 in your browser.

- Ask questions about your PDFs.

- Click the 🔄 Refresh button to re-index if you add more files.

📁 Project Structure
```graphql
./
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── pdfs/                # Place your PDFs here
└── vectorstore/         # Automatically generated local vector DB
```

## 💬 Example Questions

- "Summarize the content of all the PDFs."

- "What is the main idea in the second document?"

- "How many PDFs are loaded?"

- "What are you?"


## 🔒 Privacy

This chatbot runs entirely offline. No data is sent anywhere — your files and questions stay on your computer.

## 🙌 Credits
Built using:
- LangChain
- Ollama
- HuggingFace Transformers

🧠 Made by Satya (@programmingxpert)
with ❤️
