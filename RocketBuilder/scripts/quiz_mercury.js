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
const questionNumberElement = document.getElementById('question-number');
resultsElement.setAttribute('id', 'results');
resultsElement.classList.add('results', 'hide');
quizAppElement.appendChild(resultsElement);

let shuffledQuestions, currentQuestionIndex;
let budget = 0;
let budgetAdd = 100;

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

  }
  else {
    budgetAdd = 100;
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
  fetch("http://localhost:3000/updateStatus", {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "budget":budget,
      "currentPlanet":"Earth",
      "targetPlanet":"Mercury"
    }), // body data type must match "Content-Type" header
  })
  .then(response => {
    if (response.ok) {
      window.location.href = '../builder.html';
    }
  });
}

const questions = [{
  "question": "Mercury is the ____ planet in the Solar System? ",
  "answers": [
    { "text": "Biggest", "correct": false},
    { "text": "Second Biggest", "correct": false},
    { "text": "Smallest", "correct": true},
    { "text": "Second Smallest", "correct": false}
  ]
},
{
  "question": "How many hours are in a day on Mercury?",
  "answers": [
    { "text": "1,408", "correct": true},
    { "text": "24", "correct": false},
    { "text": "30", "correct": false},
    { "text": "3", "correct": false}
  ]
},
{
  "question": "Why does Mercury have so many craters?",
  "answers": [
    { "text": "Explosions", "correct": false},
    { "text": "Asteroid impacts", "correct": true},
    { "text": "Spinning too fast", "correct": false},
    { "text": "Too close to the sun", "correct": false}
  ]
},
{
  "question": "What is Mercury named after?",
  "answers": [
    { "text": "Roman God of Communication", "correct": true},
    { "text": "Greek God of Technology", "correct": false},
    { "text": "The element", "correct": false},
    { "text": "Celtic Word for small", "correct": false}
  ]
},
{
  "question": "What happens at Mercury's poles?",
  "answers": [
    { "text": "You spin faster", "correct": false},
    { "text": "The sun looks bigger", "correct": false},
    { "text": "They are permanently in shadow", "correct": true},
    { "text": "Magic spells", "correct": false}
  ]
},
{
  "question": "Whehn was Mercury first seen?",
  "answers": [
    { "text": "1610", "correct": true},
    { "text": "1423", "correct": false},
    { "text": "1010", "correct": false},
    { "text": "1778", "correct": false}
  ]
},
{
  "question": "What is the gravity of Mercury?",
  "answers": [
    { "text": "5.0 m/s^2", "correct": false},
    { "text": "12.2 m/s^2", "correct": false},
    { "text": "9.8 m/s^2", "correct": false},
    { "text": "3.7 m/s^2", "correct": true}
  ]
},
{
  "question": "How many Mercurys can fit into the Sun?",
  "answers": [
    { "text": "Around 30 million", "correct": false},
    { "text": "Around 13 million", "correct": false},
    { "text": "Around 21 million", "correct": true},
    { "text": "Around 5 million", "correct": false}
  ]
},
{
  "question": "What is the hottest temperature on Mercury?",
  "answers": [
    { "text": "200 Degrees", "correct": false},
    { "text": "430 Degrees", "correct": true},
    { "text": "310 Degrees", "correct": false},
    { "text": "540 Degrees", "correct": false}
  ]
},
{
  "question": "How many kilometers to walk around the entirety of Mercury?",
  "answers": [
    { "text": "2,631 km", "correct": false},
    { "text": "11,101 km", "correct": false},
    { "text": "3,041 km", "correct": false},
    { "text": "4,880 km", "correct": true}
  ]
}];