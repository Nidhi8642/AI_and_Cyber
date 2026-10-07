import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=API_KEY)

def generate_security_analysis(prompt: str) -> str:
    try:
        interaction = client.interactions.create(
            model = "gemini-3.8-flash",
            input=prompt,
            generation_config={"thinking_level" : "low"},
        )
        if interaction.output_text:
            return interaction.output_text
    except Exception as error:
        print(f"Gemini temporily unavailable: {error}")

#Safe fallback so the application remains functional
    return(
        "AI-generated analysis is temporarily unavailable because"
        "the Gemini service is currently experiencing high demand.\n\n"
        "The alert has still been processed successfully through the "
        "rule-based detection and RAG knowledge-base pipeline.\n\n"
        "Recommended next steps:\n"
        "1. Review the alert evidence.\n"
        "2. Investigate the source IP and affected account.\n"
        "3. Correlate related authentication events.\n"
        "4. Follow the relevant defensive procedures in the knowledge base.\n"
        "5. Retry AI analysis when the Gemini service becomes available."
    )
