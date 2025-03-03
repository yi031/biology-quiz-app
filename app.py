from flask import Flask, request, jsonify
from flask_cors import CORS
from hip_agent import HIPAgent
import csv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize a HIPAGENT
agent = HIPAgent()

# Load questions from testbench.csv
questions = []
with open("testbench.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        questions.append({
            'question': row['question'],
            'answers': [row['answer_0'], row['answer_1'], row['answer_2'], row['answer_3']],
            'correct': row['correct']
        })


@app.route('/question/<int:id>', methods=['GET'])
def get_question(id):
    '''Display question and options on the frontend interface.'''
    if 0 <= id < len(questions):
        return jsonify(questions[id])
    return jsonify({'error': 'Question not found'}), 404


@app.route('/help', methods=['POST'])
def get_help():
    '''Call hip_agent to get answer and explanations.'''
    data = request.json
    question = data['question']
    answers = data['answers']
    selected_index, explanation = agent.get_response(question, answers, 0)

    return jsonify({
        'response': int(selected_index),
        'explanation': explanation
    })


if __name__ == '__main__':
    app.run(debug=True)
