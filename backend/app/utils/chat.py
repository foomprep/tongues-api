from app.utils.models import get_chat_response

MISUNDERSTOOD_RESPONSE = {
    "Dutch": "Het spijt me, ik begreep je niet.",
    "English": "Sorry, I didn't understand you.",
    "French": "Je suis désolé, je ne t'ai pas compris.",
    "Spanish (American)": "Lo siento, no te entendí.",
    "Italian": "Mi dispiace, non ti ho capito.",
    "German": "Es tut mir leid, ich habe dich nicht verstanden."
}

def get_chat_response_by_language(
    text: str,
    language: str,
    history: str = None,
):
    response = get_chat_response(f"Generate a sentence to continue the following conversation in {language}. ONLY return the sentence.\n{history}Human: {text}\nAI:")
    newHistory = f"Human:{text}\nAI:{response}" if history is None else history + f"\nHuman:{text}\nAI:{response}"
    return {
        "is_valid": True,
        "grammar_correct": True,
        "history": newHistory,
        "response": response
    }

def is_valid_grammar(
    text: str,
    language: str,
) -> bool:
    response = get_chat_response(f"Does the text '{text}' contain valid grammar in the {language} language? ONLY repsond with Yes or No")
    if "No" in response:
        return False
    if "Yes" in response:
        return True

def explain_invalid_grammar(
    text: str,
    language: str,
) -> str:
    return get_chat_response(f"Explain what is wrong with the grammar in the {language} text '{text}'")
