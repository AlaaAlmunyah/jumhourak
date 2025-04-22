# 🎬 Jumhourak | AI Assistant for Saudi Filmmakers

**Jumhourak** is an AI-powered assistant built with Streamlit to help Saudi filmmakers analyze their film concepts. It generates data-driven insights using real market signals, language analysis, and audience behavior.

---

## 🔍 What Does Jumhourak Do?

- 🧠 Leverages **DeepSeek AI** to analyze Arabic film ideas and extract marketing insights tailored to audience trends
- 🎟 Pulls real-time insights from the **Saudi Box Office** (official Ministry of Culture source)
- 🎞 Matches your film with **similar successful titles** and identifies audience overlap
- 📊 Recommends optimal **distribution strategies** (platforms, timing, breakdown)
- 👥 Generates accurate **target audience profiles** (age, gender, viewing habits)
- 🇸🇦 Fully built in **Arabic-first interface** for cultural relevance

---

## 📦 Tech Stack

- `Streamlit` — for the interactive user interface
- `DeepSeek API` — for intelligent text analysis in Arabic
- `TMDb API` — for film metadata and similarity search
- `BeautifulSoup` — to scrape official Saudi box office data
- `pandas` & `re` — for data cleaning and handling

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/AlaaAlmunyah/jumhourak.git
cd jumhourak
pip install -r requirements.txt
streamlit run jumhourak.py
