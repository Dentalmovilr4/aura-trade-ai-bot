import google.generativeai as genai
import time
import os

# Configuras tu API KEY de Google AI Studio (Gratis)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

TOPICS = [
    "ganar dinero con trading automático",
    "bot de trading funcionando en vivo",
    "copy trading rentable",
    "ingresos pasivos con crypto"
]

def generate_post():
    topic = TOPICS[int(time.time()) % len(TOPICS)]
    prompt = f"Crea un guion corto estilo TikTok viral sobre {topic}. Gancho de 3 seg y CTA."
    
    response = model.generate_content(prompt)
    return response.text

while True:
    print("🎬 NUEVO CONTENIDO CON GEMINI:\n", generate_post())
    time.sleep(3600)
