from google import genai

client = genai.Client(api_key="AIzaSyAMp1GXXXACFUY_p4bI3LxuQuKgHM8n0hI")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
