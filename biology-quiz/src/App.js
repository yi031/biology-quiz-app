import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [questionId, setQuestionId] = useState(0);
  const [question, setQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [help, setHelp] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [quizEnded, setQuizEnded] = useState(false);

  useEffect(() => {
    fetchQuestion();
  }, [questionId]);

  const fetchQuestion = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/question/${questionId}`
      );
      if (response.data && Object.keys(response.data).length > 0) {
        setQuestion(response.data);
        setSelectedAnswer(null);
        setHelp(null);
        setSubmitted(false);
      } else {
        setQuizEnded(true);
      }
    } catch (error) {
      console.error("Error fetching question:", error);
      setQuizEnded(true);
    }
  };

  const handleGetHelp = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/help", {
        question: question.question,
        answers: question.answers,
      });
      setHelp(response.data);
    } catch (error) {
      console.error("Error fetching help:", error);
      // Optionally, set an error state here
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const handleNext = () => {
    if (quizEnded) {
      setQuestionId(0);
      setQuizEnded(false);
    } else {
      setQuestionId((prevId) => prevId + 1);
    }
  };

  if (!question) return <div>Loading...</div>;

  return (
    <div className="App">
      <div className="quiz-container">
        <h1>Biology Quiz</h1>
        {quizEnded ? (
          <div className="quiz-end">
            <h2>You've reached the end of the quiz!</h2>
            <p>Great job completing all the questions.</p>
            <button onClick={handleNext}>Start Over</button>
          </div>
        ) : (
          <div className="question-box">
            <h2>{question.question}</h2>
            <div className="answers">
              {question.answers.map((answer, index) => (
                <div key={index} className="answer">
                  <input
                    type="radio"
                    id={`answer${index}`}
                    name="answer"
                    value={answer}
                    checked={selectedAnswer === answer}
                    onChange={() => setSelectedAnswer(answer)}
                    disabled={submitted}
                  />
                  <label htmlFor={`answer${index}`}>{answer}</label>
                </div>
              ))}
            </div>
            <div className="buttons">
              <button onClick={handleGetHelp} disabled={submitted}>
                Get Help from AI 🤖
              </button>
              <button
                onClick={handleSubmit}
                disabled={!selectedAnswer || submitted}
              >
                Submit
              </button>
              <button onClick={handleNext} disabled={!submitted}>
                Next Question
              </button>
            </div>
          </div>
        )}

        {isLoading && <p className="loading-text">Generating help...</p>}

        {help && !quizEnded && (
          <div className="help-box">
            <h3>AI Explanation:</h3>
            <p>{help.explanation}</p>
            <p>
              <strong>Suggested answer:</strong>{" "}
              {question.answers[help.response]}
            </p>
            <p className="caution-text">
              <em>
                Note: AI can make mistakes. Please use the suggested answer with
                caution.
              </em>
            </p>
          </div>
        )}

        {submitted && !quizEnded && (
          <div className="result-box">
            <h3>Result:</h3>
            <p>
              {selectedAnswer === question.correct ? (
                <>
                  <span className="emoji">✅</span> Correct!
                </>
              ) : (
                <>
                  <span className="emoji">❌</span> Incorrect.
                </>
              )}
            </p>
            <p>
              <strong>Correct answer:</strong> {question.correct}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
