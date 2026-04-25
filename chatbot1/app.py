from openai import OpenAI
#openai package = just HTTP client with nice format.

#this does not use the memory,forget previous convo.
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")

        break

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    print("Bot:", response.choices[0].message.content)

