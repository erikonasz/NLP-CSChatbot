from flask import Flask, render_template, request
import openai
import random

app = Flask(__name__)

with open("openai.txt") as file:
    openai.api_key = file.read()

start_sequence = ""
restart_sequence = "You:"


# creating custom respones
responses = {
    # responding to greetings
    "greetings": ["Hello! How can I help you today?", "Welcome! How may I assist you?", ...],
    # responding to thanks
    "thanks": ["You're welcome!", "It was my pleasure to assist you.", ...],
}

faq = {
    "privacy": "Our privacy policy outlines how we collect and handle your personal information. You can find detailed information on our Privacy Policy page.",
    "data collection": "We collect data to improve our services and provide a better user experience. You can learn more about our data collection practices in our Terms and Conditions.",
    "cookies": "We use cookies to enhance your browsing experience. You can find detailed information about our use of cookies in our Cookie Policy.",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']

    prompt = restart_sequence + user_input

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" You:", " "]
    )

    bot_reply = response.choices[0].text.strip().replace(start_sequence, "")

    # Check if user input contains a greeting keyword
    if any(greeting in user_input.lower() for greeting in ["hello", "hi", "hey"]):
        bot_reply = random.choice(responses["greetings"])
    # Check if user input contains a thank you keyword
    elif any(thanks in user_input.lower() for thanks in ["thank you", "thanks"]):
        bot_reply = random.choice(responses["thanks"])
    else:
    # Check if user input matches any keywords in terms and conditions
        matched_keywords = [keyword for keyword in faq if keyword in user_input.lower()]
        if matched_keywords:
            bot_reply = faq[matched_keywords[0]]


    return str(bot_reply)

if __name__ == '__main__':
    app.run()