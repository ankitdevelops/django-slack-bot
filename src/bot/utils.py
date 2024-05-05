import os
from openai import OpenAI
import helpers

OPENAI_API_KEY = helpers.config("OPENAI_API_KEY", default=None)


def get_openai_client():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def chat_with_openai(message, model="gpt-3.5-turbo", raw=False):
    client = get_openai_client()
    print(os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an amazing code assistant",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        model=model,
    )
    if raw:
        return response
    print("print>>>", response.choices[0].message.content)
    return response.choices[0].message.content
