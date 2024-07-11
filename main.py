from flask import Flask, request, render_template, jsonify
import openai

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = 'your_openai_api_key'

# Function to check if a question is relevant to General Chemistry 1 and 2
def is_chemistry_question(question):
    keywords = ['mole', 'grams', 'mass', 'volume', 'concentration', 'solution', 'reaction', 'stoichiometry', 'percent', 'yield']
    return any(keyword in question.lower() for keyword in keywords)

# Function to generate a response using OpenAI
def generate_response(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer this General Chemistry question with a mathematical solution: {question}",
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    question = data.get('question', '')

    if not is_chemistry_question(question):
        return jsonify({"response": ""})

    response = generate_response(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
