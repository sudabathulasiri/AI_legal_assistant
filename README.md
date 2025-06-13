# ⚖️ AI Legal Assistant

[![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-brightgreen)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

A modern **Streamlit app** to **extract**, **translate**, **summarize**, and **analyze legal documents** with the power of AI.

---

## ✨ Features

✅ Upload PDF, image, DOCX, or TXT files  
✅ Extract text using OCR  
✅ Auto-translate to English  
✅ Summarize documents in seconds  
✅ Ask questions about your document  
✅ AI-powered legal chatbot  

---

## 📸 Demo

### ▶️ Quick Preview (GIF)

![AI Legal Assistant Demo](assests/demo.gif)

### 🎥 Full Demo Video (46 sec)

👉 [Watch the full demo video here](https://drive.google.com/file/d/1yAjBcG72s7MTcRtmrL6SwgJukzqXB2Pm/view?usp=sharing)

---

## 🚀 Quick Start

### 1️⃣ Clone the repository

```sh
git clone https://github.com/sudabathulasiri/AI_legal_assistant.git
cd AI_legal_assistant
```

### 2️⃣ Create & activate a virtual environment

```sh
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Python requirements

```sh
pip install -r requirements.txt
```

### 4️⃣ Install system dependencies

- **Tesseract OCR** (for image text extraction):
  - Windows: [Download here](https://github.com/tesseract-ocr/tesseract/wiki)
  - Ubuntu: `sudo apt-get install tesseract-ocr`
- **poppler** (for PDF to image conversion):
  - Windows: [Download here](http://blog.alivate.com.au/poppler-windows/)
  - Ubuntu: `sudo apt-get install poppler-utils`

### 5️⃣ Add your OpenRouter API key

Create a file at `.streamlit/secrets.toml` in your project root with this content:

```
OPENROUTER_API_KEY = "sk-..."
```
> **Never share your API key publicly!**

---

## ▶️ Running the App

```sh
streamlit run Legal_assist.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## 📦 Requirements

All Python dependencies are listed in `requirements.txt`.  
Main packages:
- streamlit
- openai
- pytesseract
- pdf2image
- Pillow
- langdetect
- python-docx

---

## 📝 Notes

- This tool provides information only. Always consult with qualified legal professionals for legal advice.
- If you encounter issues with OCR or PDF extraction, ensure Tesseract and poppler are installed and available in your system PATH.
- For best results, use clear, high-quality document scans.
---

## 📄 License

This project is for educational purposes. See [LICENSE](LICENSE) for details.
