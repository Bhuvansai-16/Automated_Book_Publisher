# 📚 Automated Book Publisher Workflow

Welcome to **Automated Book Publisher** – a Streamlit-powered platform that allows users to scrape book content, rewrite it using multi-agent AI workflows, and manage their personal book libraries. Built for creators, educators, and knowledge publishers who want fast and intelligent control over book workflows.

---

## 🚀 Features

- 🔧 **Scrape & Rewrite**: Enter a Wikisource URL and fetch chapter content using BeautifulSoup.
- ✍️ **Multi-Agent AI Pipeline**: The scraped content is rewritten using AI agents (Writer → Editor → Reviewer) via Gemini or your preferred LLM.
- 💾 **Version Saving**: Save final rewritten chapters under book titles. Supports multiple chapters per book.
- 📖 **Reader Mode**: Read saved chapters in fullscreen with rating and navigation (Next/Previous Chapter).
- ⭐ **RL-Based Chapter Ranking**: Rate chapters (1–10) to improve book discoverability using reinforcement-style logic.
- 🗂️ **User Libraries**: Each user sees only their own saved books and chapters.
- 🔐 **Authentication (Supabase)**: Users log in with email and password. Sessions are isolated per user.
- 📥 **Download Book**: Download the full book text as a `.txt` file.
- 📂 **My Library Dashboard**: Visual summary of saved chapters with preview and direct read links.
- 🧠 **Memory with ChromaDB**: All user sessions and saved versions are persistently stored.
- 🎯 **Production Ready**: Polished, modern UI built with modular Streamlit architecture.

---

## 🧱 Tech Stack

| Component      | Tech Used                      |
|----------------|--------------------------------|
| Frontend       | Streamlit                      |
| Backend        | Python + Streamlit             |
| LLM Interface  | Gemini                         |
| Storage        | ChromaDB                       |
| Auth & Users   | Supabase                       |
| Web Scraping   | BeautifulSoup+Playwright       |

---

## 📂 Folder Structure

AiPBook/
├── App.py # Main Streamlit app
├── scraper.py # BeautifulSoup-based content fetcher
├── rewrite_agent.py # Multi-agent AI pipeline
├── chroma_manager.py # Save/load from ChromaDB
├── .env # API keys and environment variables
├── requirements.txt
├── README.md
└── chromadb_store/ # Persistent ChromaDB storage


---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/Automated_Book_Publisher.git
cd AiPBook
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Environment Variables
```bash
GEMINI_API_KEY=your_api_key_here
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your_supabase_anon_or_service_key
```

### 5. Run the app
```bash
streamlit run app.py
```
---
🔐 Supabase Setup (Optional)
- Go to https://supabase.io and create a project.
- Enable email/password auth.
- Use your project URL and anon/public key in the .env.
---
👨‍💻 Developer Notes
- Uses RL-style chapter ranking from user feedback.
- Modular design with clear separation between scraping, AI agents, storage, and UI.
- Multi-user support with private session-based libraries.
---
📝 License
MIT License © 2025 Chilamkurthi Bhuvansai



