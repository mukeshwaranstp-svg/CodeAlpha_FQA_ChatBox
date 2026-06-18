🎩 Mugiwara FAQ Bot — CodeAlpha AI Internship Task 2

An AI-powered FAQ Chatbot built with NLP, Sentence Transformers, and Cosine Similarity — packaged as a desktop application.


📌 About This Project
This project was built as Task 2 of the CodeAlpha AI Internship Program.
The goal was to build an intelligent FAQ chatbot that doesn't just match keywords — it understands the meaning behind a question and finds the closest matching answer from a dataset using NLP and machine learning techniques.
This is not a GPT-powered chatbot. It uses vector similarity to retrieve answers from a pre-defined FAQ dataset — making it fast, offline, and cost-free to run.

🧠 What I Learned

What word embeddings are and why they exist
How cosine similarity measures meaning between sentences
Why we need NLP preprocessing before comparing text
The difference between a generative chatbot (LLM) and a retrieval chatbot (FAQ matching)
How to build and package a desktop AI application with Python
How sentence-transformers converts text into vectors
Why a threshold is needed for similarity matching
How argmax() finds the best match from a list of scores
How to use PyInstaller to package Python apps into .exe


🛠️ Tech Stack
ToolPurposePythonCore languageNLTKText preprocessing (tokenization, stopwords)Sentence Transformers (all-MiniLM-L6-v2)Convert text to vectorsScikit-learn (cosine_similarity)Measure similarity between vectorsCustomTkinterModern dark-themed desktop UIPyInstallerPackage app as .exeJSONFAQ dataset storage

📁 Project Structure
project fqa chat box/
│
├── chat.py                          # Core NLP logic
├── main.py                          # App entry point
├── ui.py                            # Basic tkinter UI (skeleton)
├── Ecommerce_FAQ_Chatbot_dataset.json  # FAQ dataset
├── requirements.txt                 # Dependencies
├── .gitignore                       # Git ignore rules
│
└── assets/
    └── straw_hat.svg               # Bot avatar

⚙️ How It Works
User types a question
        ↓
NLTK cleans the text
(lowercase → remove punctuation → tokenize → remove stopwords)
        ↓
Sentence Transformer converts it to a vector
        ↓
Cosine similarity compares it against all FAQ question vectors
        ↓
argmax() finds the highest similarity score
        ↓
If score > 0.4 → return matching answer
If score < 0.4 → "Sorry, I don't have an answer for that."

🚀 How to Install & Run
1. Clone the repository
bashgit clone https://github.com/mukeshwaranstp-svg/CodeAlpha_FQA_ChatBox.git
cd CodeAlpha_FQA_ChatBox
2. Create virtual environment
bashpython -m venv .venv
.venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Run the app
bashpython main.py

📦 Requirements
nltk
sentence-transformers
scikit-learn
customtkinter

🐛 Problems We Faced & How We Solved Them
1. Corrupted .venv
Error: SyntaxError: source code string cannot contain null bytes

Cause: Virtual environment files got corrupted during installation

Fix: Deleted and recreated the .venv from scratch
2. Missing FAQ File
Error: FileNotFoundError: faq.json

Cause: Python couldn't find the JSON file

Fix: Ensured the file was in the correct project directory and used resource_path() for PyInstaller builds
3. NLTK Missing Data
Error: Resource punkt_tab not found

Cause: Wrong NLTK package name

Fix: Changed nltk.download('punkt') to nltk.download('punkt_tab')
4. CustomTkinter Font Error
Error: Wrong font type <class 'tkinter.font.Font'>

Cause: CustomTkinter doesn't accept tkinter Font objects

Fix: Used ctk.CTkFont(size=14, weight="bold") instead
5. GitHub Push Rejected — File Too Large
Error: File exceeds GitHub's 100MB limit

Cause: .venv and dist/ folders (PyTorch = 293MB) were being pushed

Fix: Added .venv/, dist/, build/ to .gitignore and removed them from git tracking
6. EXE Couldn't Find Dataset
Error: FileNotFoundError: Ecommerce_FAQ_Chatbot_dataset.json

Cause: PyInstaller didn't bundle the dataset automatically

Fix: Used resource_path() function and --add-data flag in PyInstaller command

🎨 UI Features

Chat bubbles — user right, bot left
Quick reply buttons (Track order, Return policy, Payment methods, Shipping time)
Typing indicator animation
Straw hat avatar 🎩
Welcome message on startup


🏗️ Build EXE
bashpyinstaller --name "MugiwaraFAQBot" --onedir --windowed ^
--add-data "Ecommerce_FAQ_Chatbot_dataset.json;." ^
--add-data "assets;assets" ^
main.py

🌊 About CodeAlpha Internship
CodeAlpha is a software development company offering AI internship programs with real-world project experience.
Internship Perks:

Completion Certificate (QR Verified)
Letter of Recommendation
LinkedIn Recognition
Job Placement Support

Task List (AI Domain):

✅ Task 1: Language Translation Tool
✅ Task 2: FAQ Chatbot ← This project
🔲 Task 3: Music Generation with AI
🔲 Task 4: Object Detection and Tracking


👤 Author
Mukeshwaran

GitHub: @mukeshwaranstp-svg
Internship: CodeAlpha AI — 2025
