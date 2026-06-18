# 🎩 Mugiwara FAQ Bot — CodeAlpha AI Internship Task 2

> An AI-powered FAQ Chatbot built with NLP, Sentence Transformers, and Cosine Similarity.

---

## 📌 About This Project

Built as **Task 2** of the **CodeAlpha AI Internship Program**.

The chatbot understands the **meaning** behind a question and finds the closest matching answer from a dataset using vector similarity — not keyword matching.

---

## 🧠 What I Learned

- What **word embeddings** are and why they exist
- How **cosine similarity** measures meaning between sentences
- Why we need **NLP preprocessing** before comparing text
- The difference between a **generative chatbot** (LLM) and a **retrieval chatbot** (FAQ matching)
- How `sentence-transformers` converts text into vectors
- Why a **threshold** is needed for similarity matching
- How `argmax()` finds the best match from a list of scores
- How to package Python apps into `.exe` using PyInstaller

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| NLTK | Text preprocessing |
| Sentence Transformers | Convert text to vectors |
| Scikit-learn | Cosine similarity |
| CustomTkinter | Modern dark UI |
| PyInstaller | Package as `.exe` |
| JSON | FAQ dataset |

---

## 📁 Project Structure

```
CodeAlpha_FQA_ChatBox/
│
├── chat.py
├── main.py
├── ui.py
├── Ecommerce_FAQ_Chatbot_dataset.json
├── requirements.txt
├── .gitignore
│
└── assets/
    └── straw_hat.svg
```

---

## ⚙️ How It Works

```
User types a question
        ↓
NLTK cleans the text
        ↓
Sentence Transformer converts it to a vector
        ↓
Cosine similarity compares against all FAQ vectors
        ↓
argmax() finds the highest similarity score
        ↓
If score > 0.4 → return answer
If score < 0.4 → "Sorry, I don't have an answer for that."
```

---

## 🚀 How to Install & Run

**1. Clone the repo**
```bash
git clone https://github.com/mukeshwaranstp-svg/CodeAlpha_FQA_ChatBox.git
cd CodeAlpha_FQA_ChatBox
```

**2. Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python main.py
```

---

## 🐛 Problems & Solutions

| Problem | Cause | Fix |
|---------|-------|-----|
| `SyntaxError: null bytes` | Corrupted `.venv` | Deleted and recreated `.venv` |
| `FileNotFoundError: faq.json` | Wrong file path | Moved file to correct folder |
| `Resource punkt_tab not found` | Wrong NLTK package name | Changed to `nltk.download('punkt_tab')` |
| `Wrong font type` | CustomTkinter doesn't accept tkinter fonts | Used `ctk.CTkFont()` instead |
| GitHub push rejected (file too large) | `.venv` and `dist/` over 100MB | Added to `.gitignore` |
| EXE couldn't find dataset | PyInstaller didn't bundle JSON | Used `resource_path()` + `--add-data` flag |

---

## 🎨 UI Features

- Dark theme (`#0a0a0a` background)
- Dark green accents (`#00b300`)
- Chat bubbles — user right, bot left
- Quick reply buttons
- Typing indicator animation
- Straw hat avatar 🎩
- Welcome message on startup

---

## 🏗️ Build EXE

```bash
pyinstaller --name "MugiwaraFAQBot" --onedir --windowed --add-data "Ecommerce_FAQ_Chatbot_dataset.json;." --add-data "assets;assets" main.py
```

---

## 👤 Author

**Mukeshwaran**
GitHub: [@mukeshwaranstp-svg](https://github.com/mukeshwaranstp-svg)
Internship: CodeAlpha AI — 2025

---

*Built with 🎩 and the spirit of the Straw Hat Pirates — never give up on the dream!*
