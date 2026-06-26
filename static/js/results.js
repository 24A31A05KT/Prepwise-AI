// ===============================
// Load Data
// ===============================

const answers = JSON.parse(localStorage.getItem("interview_answers")) || [];
const feedback = JSON.parse(localStorage.getItem("interview_feedback")) || [];

console.log("Answers:", answers);
console.log("Feedback:", feedback);

// ===============================
// Calculate Scores
// ===============================

let totalScore = 0;

feedback.forEach(item => {
    totalScore += Number(item.score);
});

const averageScore =
    feedback.length > 0
        ? Math.round((totalScore / feedback.length) * 10)
        : 0;

// ===============================
// Update Summary Cards
// ===============================

document.getElementById("overallScore").innerText =
    averageScore + "%";

document.getElementById("technicalScore").innerText =
    averageScore + "%";

document.getElementById("communicationScore").innerText =
    Math.max(0, averageScore - 5) + "%";

document.getElementById("confidenceScore").innerText =
    Math.min(100, averageScore + 3) + "%";

// ===============================
// Feedback Cards
// ===============================

const container = document.getElementById("feedbackContainer");

container.innerHTML = "";

feedback.forEach((item, index) => {

    const card = document.createElement("div");

    card.className = "card shadow-lg mb-4";

    card.innerHTML = `
        <div class="card-body">

            <h3>Question ${index + 1}</h3>

            <hr>

            <h5>Your Answer</h5>
            <p>${answers[index] || "No Answer"}</p>

            <h5 class="text-primary mt-3">
                Score : ${item.score}/10
            </h5>

            <h5 class="text-success mt-3">
                Feedback
            </h5>

            <p>${item.feedback}</p>

            <h5 class="text-warning mt-3">
                Ideal Answer
            </h5>

            <p>${item.ideal_answer}</p>

        </div>
    `;

    container.appendChild(card);

});