window.addEventListener("DOMContentLoaded", async () => {
    console.log("✅ Page loaded!");

    const folderName = window.location.pathname.split("/").pop();

    try {
        const response = await fetch(`/accounts/quiz/${folderName}/`);
        const data = await response.json();

        if (data.success && data.questions.length > 0) {
            console.log("Loading saved questions...");
            data.questions.forEach(q => addQuestion(q));
        }
    } catch (error) {
        console.error("Error loading saved questions:", error);
    }
});

let questionCount = 0;
const maxQuestions = 10;

function addQuestion(q = null) {
    if (questionCount >= maxQuestions) {
        alert("Max 10 questions!");
        return;
    }

    questionCount++;

    const container = document.createElement("div");
    container.className = "question-block";
    container.id = `question-${questionCount}`;

    const optionA = q?.options ? q.options.A : '';
    const optionB = q?.options ? q.options.B : '';
    const optionC = q?.options ? q.options.C : '';

    container.innerHTML = `
        <h3>Q${questionCount}</h3>
        <input type="text" name="question${questionCount}" value="${q?.text || ''}" placeholder="Enter your question..." required><br>

        <div class="options-container">
            <label>A: <input type="text" name="optionA${questionCount}" value="${optionA}" required></label>
            <label>B: <input type="text" name="optionB${questionCount}" value="${optionB}" required></label>
            <label>C: <input type="text" name="optionC${questionCount}" value="${optionC}" required></label>
        </div>

        <label>Select Correct Option:
            <select name="correct${questionCount}" required>
                <option value="">--Select--</option>
                <option value="A" ${q?.correct_option === 'A' ? 'selected' : ''}>A</option>
                <option value="B" ${q?.correct_option === 'B' ? 'selected' : ''}>B</option>
                <option value="C" ${q?.correct_option === 'C' ? 'selected' : ''}>C</option>
            </select>
        </label>

        <button type="button" class="delete-btn">DELETE</button>
    `;

    document.getElementById("questionsContainer").appendChild(container);

    container.querySelector(".delete-btn").addEventListener("click", () => {
        container.remove();
        questionCount--;
        reNumberQuestions();
    });
}

function reNumberQuestions() {
    document.querySelectorAll(".question-block").forEach((block, index) => {
        block.querySelector("h3").innerText = `Q${index + 1}`;
    });
}

async function handleSubmit(e) {
    e.preventDefault();

    const folderName = window.location.pathname.split("/").pop();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const questions = [];

    document.querySelectorAll(".question-block").forEach(block => {
        questions.push({
            question: block.querySelector("input[name^='question']").value,
            optionA: block.querySelector("input[name^='optionA']").value,
            optionB: block.querySelector("input[name^='optionB']").value,
            optionC: block.querySelector("input[name^='optionC']").value,
            correct: block.querySelector("select[name^='correct']").value
        });
    });

    try {
        const response = await fetch('/accounts/quiz/save/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // ✅ Fix CSRF token issue
            },
            body: JSON.stringify({ folder_name: folderName, questions })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById("quizCode").textContent = data.quiz_code;
            document.getElementById("displayCode").value = data.quiz_code;
            document.getElementById("codePopup").style.display = "block";
        } else {
            alert("Error saving quiz.");
        }
    } catch (error) {
        console.error("Quiz save error:", error);
        alert("Failed to save quiz.");
    }
}

function closePopup() {
    document.getElementById("codePopup").style.display = "none";
}