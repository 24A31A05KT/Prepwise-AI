// ===============================
// Variables
// ===============================

let currentQuestion = 0;
let answers = [];
let feedback = [];

const questionElement = document.getElementById("question");
const answerElement = document.getElementById("answer");
const questionNumber = document.getElementById("questionNumber");
const totalQuestions = document.getElementById("totalQuestions");
const progressBar = document.getElementById("progressBar");

totalQuestions.innerText = QUESTIONS.length;

// ===============================
// Load Question
// ===============================

function loadQuestion() {

    questionElement.innerText = QUESTIONS[currentQuestion];

    questionNumber.innerText = currentQuestion + 1;

    answerElement.value = answers[currentQuestion] || "";

    progressBar.style.width =
        ((currentQuestion + 1) / QUESTIONS.length) * 100 + "%";
}

// ===============================
// Next
// ===============================

document.getElementById("nextBtn").onclick = () => {

    answers[currentQuestion] = answerElement.value.trim();

    if (currentQuestion < QUESTIONS.length - 1) {

        currentQuestion++;

        loadQuestion();

    }

};

// ===============================
// Previous
// ===============================

document.getElementById("prevBtn").onclick = () => {

    answers[currentQuestion] = answerElement.value.trim();

    if (currentQuestion > 0) {

        currentQuestion--;

        loadQuestion();

    }

};

// ===============================
// Finish
// ===============================

document.getElementById("finishBtn").onclick = async () => {

    answers[currentQuestion] = answerElement.value.trim();

    try {

        // Evaluate the whole interview with ONE request
        const response = await fetch("/evaluate-interview", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                questions: QUESTIONS,

                answers: answers

            })

        });

        feedback = await response.json();

        // Save locally for Results page
        localStorage.setItem(
            "interview_answers",
            JSON.stringify(answers)
        );

        localStorage.setItem(
            "interview_feedback",
            JSON.stringify(feedback)
        );

        // Save to database
        await fetch("/save-interview", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                interview_type: INTERVIEW_TYPE,

                questions: QUESTIONS,

                answers: answers,

                feedback: feedback

            })

        });

        window.location.href = "/results";

    } catch (error) {

        console.error("Interview evaluation failed:", error);

        alert("Unable to evaluate the interview. Please try again.");

    }

};

// ===============================
// Timer
// ===============================

let seconds = 600;

const timer = document.getElementById("timer");

const interval = setInterval(() => {

    const min = Math.floor(seconds / 60);

    const sec = seconds % 60;

    timer.innerText =
        `${String(min).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;

    seconds--;

    if (seconds < 0) {

        clearInterval(interval);

        document.getElementById("finishBtn").click();

    }

}, 1000);

// ===============================
// Voice Recognition
// ===============================

const voiceBtn = document.getElementById("voiceBtn");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.interimResults = false;

    recognition.continuous = false;

    voiceBtn.onclick = () => {

        recognition.start();

        voiceBtn.disabled = true;

        voiceBtn.innerHTML = "🎙 Listening...";

        document.getElementById("voiceStatus").innerHTML =
            "🎤 Listening... Speak now.";

    };

    recognition.onresult = (event) => {

        let finalTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {

            if (event.results[i].isFinal) {

                finalTranscript += event.results[i][0].transcript;

            }

        }

        answerElement.value = finalTranscript;

        document.getElementById("voiceStatus").innerHTML =
            "✅ Speech converted successfully.";

    };

    recognition.onend = () => {

        voiceBtn.disabled = false;

        voiceBtn.innerHTML = "🎤 Start Speaking";

        document.getElementById("voiceStatus").innerHTML =
            "🎤 Click microphone to continue.";

    };

    recognition.onerror = () => {

        voiceBtn.disabled = false;

        voiceBtn.innerHTML = "🎤 Start Speaking";

        document.getElementById("voiceStatus").innerHTML =
            "❌ Unable to recognize voice.";

    };

} else {

    voiceBtn.disabled = true;

    voiceBtn.innerHTML = "Voice Not Supported";

}

// ===============================
// Start
// ===============================

loadQuestion();