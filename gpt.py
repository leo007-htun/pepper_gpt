import openai

openai.api_key = ""

def chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__=="__main__":
    while True:
        user = input("U : ")
        if user.lower() in ["quit", "exit", "bye"]:
            break

        response = chat(user)
        print("bot : ", response)