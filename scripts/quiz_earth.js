document.addEventListener('DOMContentLoaded', () => {
  nextButton.classList.add('hide');
});

const startButton = document.getElementById('start');
const nextButton = document.getElementById('next');
const questionContainerElement = document.getElementById('question-div');
const questionElement = document.getElementById('question');
const answerButtonsElement = document.getElementById('question-button-div');
const quizAppElement = document.getElementById('question-app');
const resultsElement = document.createElement('div');
const budgetElement = document.getElementById('current-budget');
const streakElement = document.getElementById('current-streak');
const questionNumberElement = document.getElementById('question-number');
resultsElement.setAttribute('id', 'results');
resultsElement.classList.add('results', 'hide');
quizAppElement.appendChild(resultsElement);

let shuffledQuestions, currentQuestionIndex;
let budget = 0;
let budgetAdd = 100;
let streak = 0;

startButton.addEventListener('click', startGame);
nextButton.addEventListener('click', () => {
  currentQuestionIndex++;
  setNextQuestion();
});

function startGame() {
  startButton.classList.add('hide');
  shuffledQuestions = questions.sort(() => Math.random() - .5);
  currentQuestionIndex = 0;
  questionContainerElement.classList.remove('hide');
  setNextQuestion();
}

function setNextQuestion() {
  resetState();
  showQuestion(shuffledQuestions[currentQuestionIndex]);
}

function resetState() {
  clearStatusClass(document.body);
  nextButton.classList.add('hide');
  while (answerButtonsElement.firstChild) {
      answerButtonsElement.removeChild(answerButtonsElement.firstChild);
  }
}

function showQuestion(question) {
  questionNumberElement.innerHTML = `Question ${currentQuestionIndex+1} / ${shuffledQuestions.length}:`;
  questionElement.innerText = question.question;
  question.answers.forEach(answer => {
      const button = document.createElement('button');
      button.innerText = answer.text;
      button.classList.add('btn');
      if (answer.correct) {
          button.dataset.correct = answer.correct;
      }
      button.addEventListener('click', () => selectAnswer(button));
      answerButtonsElement.appendChild(button);
  });
}

function selectAnswer(selectedButton) {
  Array.from(answerButtonsElement.children).forEach(button => {
      button.disabled = true;
      setStatusClass(button, button.dataset.correct);
  });

  const correct = selectedButton.dataset.correct;
  if (correct) {
      budget += budgetAdd;
      budgetElement.innerHTML = `£${budget}`;
      budgetAdd += 100;
      streak += 1;
      streakElement.innerHTML = `${streak}`;


  }
  else {
    budgetAdd = 100;
    streakElement.innerHTML = `0`;
  }

  setStatusClass(selectedButton, correct);

  setTimeout(() => {
      if (shuffledQuestions.length > currentQuestionIndex + 1) {
          nextButton.classList.remove('hide');
      } else {
          concludeQuiz();
      }
  }, 1000); 
 
}

function setStatusClass(element, correct) {
  clearStatusClass(element);
  if (correct) {
      element.classList.add('correct');
  } else {
      element.classList.add('wrong');
  }
}

function clearStatusClass(element) {
  element.classList.remove('correct');
  element.classList.remove('wrong');
}

function concludeQuiz() {
  questionContainerElement.classList.add('hide');
  nextButton.classList.add('hide');

  resultsElement.classList.remove('hide');
  resultsElement.innerHTML = `
      <h2>Quiz Completed!</h2>
      <p>Your final budget: ${budget}</p>
      <button onclick="nextPage()">Build your Ship</button>
  `;
  quizAppElement.appendChild(resultsElement);
}

function nextPage() {
  fetch("../main/current_info.json")
  .then(data => {
    console.log(data);
    data.budget = budget;
  })
  window.location.href = 'builder2.html';
}

const questions = [{
  "question": "What allows us to breathe on Earth?",
  "answers": [
    { "text": "Oxygen", "correct": true},
    { "text": "Magic", "correct": false},
    { "text": "Nitrogen", "correct": false},
    { "text": "Space", "correct": false}
  ]
},
{
  "question": "What is the average temperature of Earth?",
  "answers": [
    { "text": "1000 Degrees", "correct": false},
    { "text": "15 Degrees", "correct": true},
    { "text": "12 Degrees", "correct": false},
    { "text": "25 Degrees", "correct": false}
  ]
},
{
  "question": "How many hours are in a day on Earth?",
  "answers": [
    { "text": "12", "correct": false},
    { "text": "20", "correct": false},
    { "text": "30", "correct": false},
    { "text": "24", "correct": true}
  ]
},
{
  "question": "Why is a day the length that it is?",
  "answers": [
    { "text": "Time taken for the earth to spin once", "correct": true},
    { "text": "Time taken for the earth to go around the sun", "correct": false},
    { "text": "Time taken for moon to go around the earth", "correct": false},
    { "text": "Time taken for sun to go around the earth.", "correct": false}
  ]
},
{
  "question": "What is Earth named after?",
  "answers": [
    { "text": "Roman God Terra", "correct": true},
    { "text": "Greek God Gaia", "correct": false},
    { "text": "Itself", "correct": false},
    { "text": "The Middle English word Ertha", "correct": false}
  ]
},
{
  "question": "How many species are there on Earth?",
  "answers": [
    { "text": "Around 1.5 million", "correct": false},
    { "text": "Around 2.1 million", "correct": true},
    { "text": "Around 4.6 million", "correct": false},
    { "text": "We aren't fully sure", "correct": true}
  ]
},
{
  "question": "What moon phase is this?",
  "answers": [
    { "text": "Full Moon", "correct": false},
    { "text": "New Moon", "correct": false},
    { "text": "Crescent", "correct": true},
    { "text": "Gibbous", "correct": false}
  ]
},
{
  "question": "What is the gravity of Earth?",
  "answers": [
    { "text": "5.0 m/s^2", "correct": false},
    { "text": "13.1 m/s^2", "correct": false},
    { "text": "9.8 m/s^2", "correct": true},
    { "text": "11.7 m/s^2", "correct": false}
  ]
},
{
  "question": "How many Earths can fit into the Sun?",
  "answers": [
    { "text": "Around 3 million", "correct": false},
    { "text": "Around 1.3 million", "correct": true},
    { "text": "Around 2.2 million", "correct": false},
    { "text": "Around 4.2 million", "correct": false}
  ]
},
{
  "question": "How many kilometers to walk around the entire Earth?",
  "answers": [
    { "text": "62,631 km", "correct": false},
    { "text": "44,111 km", "correct": false},
    { "text": "35,021 km", "correct": false},
    { "text": "40,007 km", "correct": true}
  ]
}];

/*const questions = [
  {
      question: "What is a Variable in JavaScript?",
      answers: [
          { text: "A section of the webpage", correct: false },
          { text: "A container for storing data values", correct: true },
          { text: "A type of JavaScript function", correct: false },
          { text: "An operation in mathematics", correct: false }
      ]
  },
  {
      question: "Which of the following is used to declare a variable in JavaScript?",
      answers: [
          { text: "var", correct: false },
          { text: "let", correct: false },
          { text: "const", correct: false },
          { text: "All of the above", correct: true }
      ]
  },
  {
      question: "What does the `===` operator check?",
      answers: [
          { text: "Only value equality", correct: false },
          { text: "Only type equality", correct: false },
          { text: "Both value and type equality", correct: true },
          { text: "Neither value nor type equality", correct: false }
      ]
  },
  {
      question: "What is an Array in JavaScript?",
      answers: [
          { text: "A function that performs an operation", correct: false },
          { text: "A single variable used to store different elements", correct: true },
          { text: "A series of characters", correct: false },
          { text: "A conditional statement", correct: false }
      ]
  },
  {
      question: "Which method can add one or more elements to the end of an array?",
      answers: [
          { text: "array.unshift()", correct: false },
          { text: "array.push()", correct: true },
          { text: "array.pop()", correct: false },
          { text: "array.slice()", correct: false }
      ]
  },
  {
      question: "How do you create a function in JavaScript?",
      answers: [
          { text: "function myFunction()", correct: true },
          { text: "create myFunction()", correct: false },
          { text: "function: myFunction()", correct: false },
          { text: "function = myFunction()", correct: false }
      ]
  },
  {
      question: "Which statement is used to execute actions based on a condition?",
      answers: [
          { text: "for", correct: false },
          { text: "while", correct: false },
          { text: "if", correct: true },
          { text: "switch", correct: false }
      ]
  },
  {
      question: "What is the purpose of a loop in JavaScript?",
      answers: [
          { text: "To perform a single action once", correct: false },
          { text: "To store multiple values in a single variable", correct: false },
          { text: "To execute a block of code a number of times", correct: true },
          { text: "To speed up code execution", correct: false }
      ]
  },
  {
      question: "Which object is the top-level object in a browser environment?",
      answers: [
          { text: "Document", correct: false },
          { text: "Window", correct: true },
          { text: "Console", correct: false },
          { text: "Navigator", correct: false }
      ]
  },
  {
      question: "What is the correct syntax for referring to an external script called `app.js`?",
      answers: [
          { text: "<script href='app.js'>", correct: false },
          { text: "<script source='app.js'>", correct: false },
          { text: "<script src='app.js'>", correct: true },
          { text: "<script link='app.js'>", correct: false }
      ]
  }
];*/