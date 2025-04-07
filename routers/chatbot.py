from fastapi import WebSocket
import json

# Simple multilingual response templates
REPLIES = {
    "en": {
        "greet": "Hello! How can I help you with your loan today?",
        "loan_help": "You can apply for a loan, check loan status, or update your profile.",
        "fallback": "Sorry, I didn’t understand that. Please try again.",
    },
    "es": {
        "greet": "¡Hola! ¿Cómo puedo ayudarte con tu préstamo hoy?",
        "loan_help": "Puedes solicitar un préstamo, verificar el estado o actualizar tu perfil.",
        "fallback": "Lo siento, no entendí eso. Inténtalo de nuevo.",
    },
    "fr": {
        "greet": "Bonjour ! Comment puis-je vous aider avec votre prêt aujourd'hui ?",
        "loan_help": "Vous pouvez demander un prêt, vérifier le statut ou mettre à jour votre profil.",
        "fallback": "Désolé, je n'ai pas compris. Veuillez réessayer.",
    },
}

# Simple rule-based intent matcher
def get_intent(message: str):
    msg = message.lower()
    if "hello" in msg or "hi" in msg:
        return "greet"
    if "loan" in msg or "help" in msg or "status" in msg:
        return "loan_help"
    return "fallback"

async def handle_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            parsed = json.loads(data)

            message = parsed.get("message", "")
            language = parsed.get("language", "en")

            intent = get_intent(message)
            reply = REPLIES.get(language, REPLIES["en"]).get(intent, REPLIES["en"]["fallback"])

            await websocket.send_text(json.dumps({
                "response": reply
            }))
    except Exception as e:
        await websocket.close()
