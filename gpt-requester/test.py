import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ["OPENAI_SECRET_KEY"],
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Who is Elon Musk?",
        }
    ],
    model="gpt-3.5-turbo",
)
print(chat_completion)