import datetime  # Optional for potential future modifications
from main_nltk import main
from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')

import os
my_api_key_gemini = "AIzaSyDqOXSiBvHUPyCGi5lhLKpYVITmRI1BkZo"

genai.configure(api_key=my_api_key_gemini)

app = Flask(__name__)

# Define your 404 error handler to redirect to the index page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    prompt = "Act as a friend and have a talk with me reply me under 50 words "

    if request.method == 'POST':
        try:
            i = 0
            user_prompt = request.form['prompt']  # Changed to user_prompt for clarity
            if i == 0:
                question = prompt + "\n" + user_prompt  # Combine prompts
                i = i + 1
            else:
                question = prompt
            response = model.generate_content(question)

            if response.text:
                # Save prompt and response to "prompts.txt"
                filename = os.path.join(os.path.dirname(__file__), "prompts.txt")  # Using absolute path
                with open(filename, "a", encoding="utf-8") as f:  # Open in append mode
                    f.write(user_prompt + "\n\n")

                return response.text
            else:
                return "Sorry, but I think Gemini didn't want to answer that!"
        except Exception as e:
            return "Sorry, but Gemini didn't want to answer that!"

    return render_template('index.html', prompt=prompt)  # Pass prompt to template

question1 = "i am stressed ,reply with me that iam stressed and suggest me a advice to reduce stress"
question2 = "i am free from stress  and reply me with that i am stress free and suggest me a motivational quote"

@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    if main():
        response = model.generate_content(question1)
        with open("./prompts.txt", "w", encoding="utf-8") as f:  # Open in write mode to clear
            f.write("")
            f.close()
        return response.text
    else:
        response = model.generate_content(question2)
        with open("./prompts.txt", "w", encoding="utf-8") as f:  # Open in write mode to clear
            f.write("")
            f.close()
        return response.text


if __name__ == '__main__':
    app.run(debug=True)
