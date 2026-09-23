# AI Screen Time Balance Advisor

Student project using LangChain/LLM and genuine Fuzzy Logic.

Supported providers:
- OpenAI
- Groq
- Google Gemini

Setup:
1. Create/activate a Python virtual environment.
2. Run: pip install -r requirements.txt
3. Copy .env.example to .env
4. Set LLM_PROVIDER and the matching API key.
5. Run: streamlit run app.py

Important: API keys must be valid and have available provider quota. The program cannot bypass provider billing or quota limits.

Project flow:
Natural language -> LangChain/LLM -> extracted values -> fuzzy membership functions -> fuzzy rules -> aggregation -> centroid defuzzification -> balance score -> AI explanation.
