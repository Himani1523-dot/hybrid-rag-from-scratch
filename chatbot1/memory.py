from openai import OpenAI

#this use  memory,keep the previous convo in the conversation list,so the bot can remember the context of the conversation and provide more relevant responses.

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

#our memory
conversation = [
    {"role": "system", "content": "You are a helpful assistant"}
]          
print("Chatbot ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # store user message
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="local-model",
        messages=conversation
    )

    reply = response.choices[0].message.content

    print("Bot:", reply, "\n")

    # store bot reply
    conversation.append({"role": "assistant", "content": reply})