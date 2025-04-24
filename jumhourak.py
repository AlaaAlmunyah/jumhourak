import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re

# ---- Page Config ----
st.set_page_config(layout="wide", page_title="FilmScope AI")

# ---- API KEYS ----
TMDB_API_KEY = "API_KEY"
DEEPSEEK_API_KEY = "sk-API_KEY"

# ---- Get Box Office Data ----
def get_box_office_data():
    url = "https://film.moc.gov.sa/en/Box-Office"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if table is None:
        return pd.DataFrame([])
    rows = table.find_all('tr')[1:]
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            data.append({
                "title": cols[0].text.strip(),
                "genre": cols[1].text.strip(),
                "tickets": int(cols[2].text.replace(',', '').strip()),
                "revenue": float(cols[3].text.replace('$', '').replace(',', '').strip()),
                "distributor": cols[4].text.strip(),
            })
    return pd.DataFrame(data)

# ---- Analyze Film with DeepSeek ----
def analyze_with_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt_text = f"""
    Analyze this film concept based on Saudi box office trends.

    Film idea: {prompt}

    Return ONLY the following in JSON format:
    {{
      "target_audience": {{"age_group": "...", "gender_split": "...", "viewing_habits": "..."}},
      "distribution_strategy": {{"platform": "...", "season": "...", "breakdown": {{"theatrical": ..., "streaming": ..., "VOD": ...}}}},
      "market_insights": {{"expected_box_office": "...", "budget": "...", "roi": "...", "sentiment": "..."}},
      "similar_films": ["..."]
    }}
    """
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt_text}]
    }

    response = requests.post(url, headers=headers, json=payload)
    text_output = response.json()['choices'][0]['message']['content']

    # استخدم try-catch للتعامل مع النصوص غير القياسية
    try:
        # محاولة إصلاح التنسيق يدويًا:
        clean = text_output.strip()
        if clean.startswith("```json"):
            clean = clean.replace("```json", "").replace("```", "")
        fixed_json = re.sub(r"(\w+):", r'"\1":', clean)  # key: → "key":
        fixed_json = fixed_json.replace("'", '"')  # توحيد علامات الاقتباس
        fixed_json = fixed_json.replace("True", "true").replace("False", "false")
        return json.loads(fixed_json), None
    except Exception as e:
        return None, text_output

# ---- Load Box Office (optional)
box_office_df = get_box_office_data()

# ---- UI Layout ----
st.title("🎬 FilmScope AI")
user_prompt = st.text_input("📝 اكتب فكرة فيلمك بالعربي:")

if st.button("🔍 تحليل الفكرة") and user_prompt:
    with st.spinner("جارٍ تحليل فكرتك باستخدام الذكاء الاصطناعي وبيانات السوق..."):
        result, raw_output = analyze_with_deepseek(user_prompt)

        if result:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🎞 أفلام مشابهة")
                for i, title in enumerate(result.get("similar_films", [])):
                    match_score = 90 - i * 5
                    st.markdown(f"**{title}**")
                    st.progress(match_score / 100, text=f"{match_score}% تشابه")

            with col2:
                st.markdown("### 👥 الجمهور المستهدف")
                audience = result.get("target_audience", {})
                st.write("**الفئة العمرية:**", audience.get("age_group", "-"))
                st.write("**نسبة الجنس:**", audience.get("gender_split", "-"))
                st.write("**عادات المشاهدة:**", audience.get("viewing_habits", "-"))

            col3, col4 = st.columns(2)
            with col3:
                st.markdown("### 🚀 استراتيجية التوزيع")
                dist = result.get("distribution_strategy", {})
                st.write("**أفضل منصة:**", dist.get("platform", "-"))
                st.write("**الموسم المقترح:**", dist.get("season", "-"))
                breakdown = dist.get("breakdown", {})
                for k, v in breakdown.items():
                    try:
                        val = float(v)
                        st.progress(val / 100, text=f"{k.upper()}: {val}%")
                    except:
                        st.write(f"{k.upper()}: {v}")

            with col4:
                st.markdown("### 📊 رؤى السوق")
                market = result.get("market_insights", {})
                st.write("**إيرادات متوقعة:**", market.get("expected_box_office", "-"))
                st.write("**ميزانية الإنتاج:**", market.get("budget", "-"))
                st.write("**العائد على الاستثمار (ROI):**", market.get("roi", "-"))
                st.write("**انطباع السوق:**", market.get("sentiment", "-"))
        else:
            st.error("❌ لم نتمكن من قراءة النتائج من DeepSeek. راجع التنسيق.")
            st.code(raw_output)

st.caption("👩‍💻 تم التصميم بواسطة ألاء • منصة جمهورك • بالاعتماد على TMDb و DeepSeek")
