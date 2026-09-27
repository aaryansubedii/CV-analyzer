const API_URL = "http://127.0.0.1:8000/analyze";

const form = document.getElementById("analyze-form");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const resultContent = document.getElementById("result-content");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const jobDescription = document.getElementById("job-description").value;
    const cvFile = document.getElementById("cv-file").files[0];

    if (!cvFile) {
        alert("Please upload a CV file.");
        return;
    }

    const formData = new FormData();
    formData.append("job_description", jobDescription);
    formData.append("cv_file", cvFile);

    resultDiv.classList.add("hidden");
    loading.classList.remove("hidden");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Analysis failed");
        }

        const data = await response.json();
        resultContent.textContent = data.analysis;
        resultDiv.classList.remove("hidden");
    } catch (err) {
        resultContent.textContent = "Something went wrong. Make sure the backend is running.";
        resultDiv.classList.remove("hidden");
    } finally {
        loading.classList.add("hidden");
    }
});