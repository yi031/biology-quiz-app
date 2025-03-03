# AI-assisted Biology Quiz Application

A web-based biology quiz application with AI assistance.

## Features

- Multiple-choice biology questions
- AI-powered help and explanations
- Interactive user interface

---

## Implementation

Modifications made to the code to make it "better":

_GPT Integration (hip_agent.py)_

- The agent retrieves relevant context from the textbook.txt using TF-IDF similarity.
- It constructs a prompt with the question, answer choices, and relevant context, and sent it to the OpenAI API (GPT-3.5-turbo) for processing.
- The response is parsed to extract the final answer and explanation.
- The final answer is compared to the given choices using embedding similarity, and the index of the most similar answer choice and the explanation are returned.

This implementation balances simplicity and functionality. It leverages GPT's pre-trained knowledge and relevant textbook context, guiding the model to answer questions with step-by-step reasoning. This approach improves processing speed and answer accuracy.

_User Interface_

- Users interact with the interface to take a multiple-choice question quiz by selecting one of the options.
- Users can "get help from AI" to receive suggested answers and explanations.
- Users then submit their answer and see the results.
- Users proceed to the next question using the "Next Question" button.

The user interface creates an intuitive and engaging quiz-taking experience. It offers clear options for answering questions, requesting AI help, and quiz navigation, empowering users to leverage AI while cautioning about potential AI mistakes.

---

## Usage

- Make sure you have a openaikey.txt in the directory.
- Run `pip install -r requirements.txt` to install backend dependencies.
- Run `pip install openai==0.28` to make sure you use the correct version of OpenAI model for this app.
- Run `python testbench.py` to get test score.
- Run `python app.py` to launch the backend server.
- In a separate terminal, `cd biology-quiz` to navigate to the frontend folder. First, run `npm install` to install frontend dependencies, and run `npm start` to launch the interface.
