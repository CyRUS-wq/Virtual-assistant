from openai import OpenAI

client = OpenAI(
    api_key="key",
)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a voice assistant."},
        {
            "role": "user",
            "content": "what is one piece."
        }
    ]
)
