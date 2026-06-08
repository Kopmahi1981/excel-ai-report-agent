import os
import google.generativeai as genai
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_ai_report(df):

    try:

        sample_data = df.head(20).to_string()

        prompt = f"""
        Analyze this investment dataset.

        Provide:
        1. Executive Summary
        2. Key Trends
        3. Important Insights
        4. Business Recommendations

        Dataset:
        {sample_data}
        """
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI ERROR: {str(e)}"