import streamlit as st
from llm_parser import extract_day_data, generate_explanation
from fuzzy_logic import evaluate_balance


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Screen Time Balance Advisor",
    page_icon="📱",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ---------- MAIN PAGE ---------- */

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ---------- GENERAL TEXT ---------- */

p {
    color: #1f2937;
}

h1, h2, h3 {
    color: #111827 !important;
}


/* ---------- HERO ---------- */

.hero-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.hero-title {
    color: white !important;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    color: white !important;
    font-size: 17px;
}


/* ---------- INPUT SECTION ---------- */

.section-title {
    color: #111827 !important;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 5px;
}

.section-description {
    color: #374151 !important;
    font-size: 16px;
    margin-bottom: 12px;
}


/* ---------- TEXT AREA ---------- */

.stTextArea textarea {
    background-color: white !important;
    color: #111827 !important;
    border: 2px solid #d1d5db !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    padding: 15px !important;
}

.stTextArea textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}


/* ---------- BUTTON ---------- */

.stButton > button {
    background: linear-gradient(
        135deg,
        #667eea,
        #764ba2
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    height: 50px !important;
}

.stButton > button:hover {
    color: white !important;
}


/* ---------- INFORMATION CARDS ---------- */

.info-card {
    padding: 25px;
    border-radius: 18px;
    min-height: 135px;
    box-shadow: 0 7px 20px rgba(0,0,0,0.10);
}

.card-title {
    color: white !important;
    font-size: 15px;
    font-weight: 700;
}

.card-value {
    color: white !important;
    font-size: 32px;
    font-weight: 800;
    margin-top: 12px;
}


/* ---------- CARD COLORS ---------- */

.screen-card {
    background: linear-gradient(135deg, #ff6b6b, #ee5253);
}

.study-card {
    background: linear-gradient(135deg, #4facfe, #00c6ff);
}

.sleep-card {
    background: linear-gradient(135deg, #8e7dff, #5f4bb6);
}

.score-card {
    background: linear-gradient(135deg, #11998e, #38ef7d);
}

.level-card {
    background: linear-gradient(135deg, #f7971e, #ffd200);
}


/* ---------- AI ADVISOR ---------- */

.ai-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 7px 20px rgba(0,0,0,0.10);
}

.ai-title {
    color: white !important;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 15px;
}

.ai-text {
    color: white !important;
    font-size: 16px;
    line-height: 1.8;
}


/* ---------- RECOMMENDATIONS ---------- */

.recommendation-box {
    background: white;
    color: #111827 !important;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 12px;
    border-left: 6px solid #667eea;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

.recommendation-text {
    color: #111827 !important;
    font-size: 16px;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827,
        #312e81
    );
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: white !important;
}


/* ---------- PROGRESS ---------- */

.stProgress > div > div > div > div {
    background-color: #667eea !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📱 Balance Advisor")

    st.divider()

    st.subheader("🧠 About")

    st.write(
        "AI Screen Time Balance Advisor analyzes "
        "your screen time, study time and sleep "
        "using Gemini and Fuzzy Logic."
    )

    st.divider()

    st.subheader("⚙️ Technology")

    st.write("🤖 Google Gemini")
    st.write("🧠 Fuzzy Logic")
    st.write("🔗 LangChain")
    st.write("🐍 Python")
    st.write("🎨 Streamlit")

    st.divider()

    st.subheader("📌 How It Works")

    st.write("1️⃣ Describe your day")
    st.write("2️⃣ Gemini extracts information")
    st.write("3️⃣ Fuzzy Logic calculates balance")
    st.write("4️⃣ AI generates explanation")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero-box">
<div class="hero-title">📱 AI Screen Time Balance Advisor</div>
<div class="hero-subtitle">
Understand your daily lifestyle balance using
Artificial Intelligence and Fuzzy Logic.
</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# INPUT
# ============================================================

st.markdown(
    """
<div class="section-title">📝 Describe Your Day</div>
<div class="section-description">
Enter your daily routine in normal language.
</div>
""",
    unsafe_allow_html=True
)


text = st.text_area(
    "Daily routine",
    placeholder=(
        "Example: I used my phone for 6 hours, "
        "studied for 4 hours and slept for 7 hours."
    ),
    height=130,
    label_visibility="collapsed"
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 Analyze My Day",
    type="primary",
    use_container_width=True
):

    if not text.strip():

        st.warning("⚠️ Please describe your day first.")

        st.stop()


    try:

        # ====================================================
        # GEMINI EXTRACTION
        # ====================================================

        with st.spinner(
            "🤖 Gemini is analyzing your routine..."
        ):

            data = extract_day_data(text)


        # ====================================================
        # FUZZY LOGIC
        # ====================================================

        with st.spinner(
            "🧠 Fuzzy Logic is calculating your balance..."
        ):

            result = evaluate_balance(
                data["screen_time_hours"],
                data["study_time_hours"],
                data["sleep_hours"]
            )


        # ====================================================
        # AI EXPLANATION
        # ====================================================

        with st.spinner(
            "💡 Generating personalized explanation..."
        ):

            explanation = generate_explanation(
                data,
                result
            )


        # ====================================================
        # SUCCESS
        # ====================================================

        st.success(
            "🎉 Analysis completed successfully!"
        )

        st.divider()


        # ====================================================
        # DAILY INFORMATION
        # ====================================================

        st.markdown(
            """
<h2>📊 Your Daily Information</h2>
""",
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(3)


        # SCREEN TIME
        with col1:

            st.markdown(
                f"""
<div class="info-card screen-card">
<div class="card-title">📱 SCREEN TIME</div>
<div class="card-value">
{data["screen_time_hours"]:.1f} hrs
</div>
</div>
""",
                unsafe_allow_html=True
            )


        # STUDY TIME
        with col2:

            st.markdown(
                f"""
<div class="info-card study-card">
<div class="card-title">📚 STUDY TIME</div>
<div class="card-value">
{data["study_time_hours"]:.1f} hrs
</div>
</div>
""",
                unsafe_allow_html=True
            )


        # SLEEP
        with col3:

            st.markdown(
                f"""
<div class="info-card sleep-card">
<div class="card-title">😴 SLEEP</div>
<div class="card-value">
{data["sleep_hours"]:.1f} hrs
</div>
</div>
""",
                unsafe_allow_html=True
            )


        st.write("")

        st.divider()


        # ====================================================
        # BALANCE ANALYSIS
        # ====================================================

        st.markdown(
            """
<h2>🎯 Balance Analysis</h2>
""",
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)


        # SCORE
        with col1:

            st.markdown(
                f"""
<div class="info-card score-card">
<div class="card-title">🎯 BALANCE SCORE</div>
<div class="card-value">
{result["score"]}/100
</div>
</div>
""",
                unsafe_allow_html=True
            )


        # LEVEL
        with col2:

            st.markdown(
                f"""
<div class="info-card level-card">
<div class="card-title">📌 BALANCE LEVEL</div>
<div class="card-value">
{result["level"]}
</div>
</div>
""",
                unsafe_allow_html=True
            )


        st.write("")


        # PROGRESS BAR

        score = int(result["score"])

        score = max(
            0,
            min(score, 100)
        )

        st.progress(score)

        st.caption(
            f"Balance score: {score}/100"
        )


        st.divider()


        # ====================================================
        # AI ADVISOR
        # ====================================================

        st.markdown(
            """
<h2>🤖 AI Advisor</h2>
""",
            unsafe_allow_html=True
        )


        # IMPORTANT:
        # Display explanation separately.
        # This prevents Markdown/code formatting problems.

        st.markdown(
            f"""
<div class="ai-box">
<div class="ai-title">
✨ Personalized Analysis
</div>
</div>
""",
            unsafe_allow_html=True
        )


        # Show Gemini response as normal text/Markdown
        st.markdown(explanation)


        st.divider()


        # ====================================================
        # QUICK RECOMMENDATIONS
        # ====================================================

        st.markdown(
            """
<h2>💡 Quick Recommendations</h2>
""",
            unsafe_allow_html=True
        )


        recommendations = []


        # HIGH SCREEN TIME

        if data["screen_time_hours"] > 6:

            recommendations.append(
                "📱 Consider reducing unnecessary screen time."
            )


        # LOW STUDY TIME

        if data["study_time_hours"] < 3:

            recommendations.append(
                "📚 Try to create a consistent study schedule."
            )


        # LOW SLEEP

        if data["sleep_hours"] < 7:

            recommendations.append(
                "😴 Try to maintain a regular sleep routine."
            )


        # BALANCED

        if not recommendations:

            recommendations.append(
                "✅ Your reported routine is reasonably balanced."
            )


        # DISPLAY

        for recommendation in recommendations:

            st.markdown(
                f"""
<div class="recommendation-box">
<div class="recommendation-text">
{recommendation}
</div>
</div>
""",
                unsafe_allow_html=True
            )


        # ====================================================
        # FOOTER
        # ====================================================

        st.divider()

        st.markdown(
            """
<div style="text-align:center; color:#6b7280; padding:20px;">
📱 <b>AI Screen Time Balance Advisor</b>
<br>
Gemini + LangChain + Fuzzy Logic + Streamlit
</div>
""",
            unsafe_allow_html=True
        )


    except Exception as e:

        st.error(
            f"❌ Analysis failed: {e}"
        )