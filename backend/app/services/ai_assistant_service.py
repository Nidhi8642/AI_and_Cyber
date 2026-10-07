from app.rag.retriever import search_knowledge_base
from app.services.gemini_service import generate_security_analysis

def build_security_prompt(event_type: str, severity: str, message: str) -> dict:
    query = f"{event_type} {message}"
    knowledge = search_knowledge_base(query=query, top_k=3)
    context = "\n\n".join(
        f"Source: {item['source']}\n{item['content']}"
        for item in knowledge
    )
    prompt = f"""
    You are a cybersecurity analyst assistant.
    Analyze the following security event using ONLY the information provided in the event and the retrieved security knowledge.
    EVENT
    Event Type: {event_type}
    Severity: {severity}
    Message: {message}

    RETRIVED SECURITY KNOWLEDGE : {context}

    Provide your analysis using exactly these sections:
    1. Threat Explanation
    Explain what the event means and what threat it may represent.

    2. Why this event is suspicious
    Explain the specific indicators present in the provided event.
    Do not add indicators that are not present.

    3. Investigation Steps
    Give practical steps a security analyst should perform.
    Do not claim that an investogation has already been performed.

    4. Recommended Defensive Actions
    Give safe defensive recommendations.
    Do not perform or recommend destructive or irreversibble actions.

    5. Risk Assessment
    Explain the potential impact and urgency based only on the available evidence.

    
    STRICT Rules:
    - Use only evidence present in the event or retrieved knowledge.
    - Do not invent facts, users, systems, locations, timestamps,
    attack techniques, or investigation results.
    - Do not infer that an IP address is internal, external, malicious,
    trusted, or compromised unless this is explicitly established
    by the provided information.
    - Do not assume that an account is compromised unless evidence
    indicates successful unauthorized access or compromise.
    - Clearly distinguish between observed evidence and possible scenarios.
    - Use phrases such as "may indicate", "could suggest", or
    "requires investigation" when something is uncertain.
    - Do not claim an action was performed when it is only a recommendation.
    - Do not recommend destructive or irreversible actions.
    - Keep the final decision with a human security analyst.
    """
    analysis = generate_security_analysis(prompt)
     
    return{
        "analysis" : analysis,
        "prompt" : prompt.strip(),
        "knowledge" : knowledge
    }