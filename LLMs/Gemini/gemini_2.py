from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List the top 5 largest cities in the world by population.",
)

print(response.text)