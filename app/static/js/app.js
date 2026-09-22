const examples = {
  positive: "The room was clean, the staff were friendly, and the location was excellent.",
  negative: "The room was noisy, the bathroom was dirty, and the service was disappointing.",
  mixed: "The location was great, but the room was small and the staff were not very helpful.",
};

const reviewText = document.querySelector("#review-text");
const characterCount = document.querySelector("#character-count");
const analyzeButton = document.querySelector("#analyze-button");
const clearButton = document.querySelector("#clear-button");
const formMessage = document.querySelector("#form-message");
const resultPanel = document.querySelector("#result-panel");
const resultPlaceholder = resultPanel.querySelector(".result-placeholder");
const resultContent = resultPanel.querySelector(".result-content");

function updateCharacterCount() {
  characterCount.textContent = `${reviewText.value.length} characters`;
}

function setMessage(message = "", type = "") {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type}`.trim();
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.classList.toggle("is-loading", isLoading);
  analyzeButton.querySelector(".button-label").textContent = isLoading
    ? "Analyzing sentiment..."
    : "Analyze sentiment";
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function showResult(prediction) {
  const isPositive = prediction.label === "positive";
  const positive = prediction.probabilities.positive;
  const negative = prediction.probabilities.negative;

  resultPanel.classList.remove("is-empty", "negative");
  resultPanel.classList.toggle("negative", !isPositive);
  resultPlaceholder.hidden = true;
  resultContent.hidden = false;
  document.querySelector("#sentiment-label").textContent = isPositive ? "Positive" : "Negative";
  document.querySelector("#sentiment-icon").textContent = isPositive ? "✓" : "!";
  document.querySelector("#confidence-value").textContent = formatPercent(prediction.confidence);
  document.querySelector("#positive-probability").textContent = formatPercent(positive);
  document.querySelector("#negative-probability").textContent = formatPercent(negative);

  window.requestAnimationFrame(() => {
    document.querySelector("#positive-bar").style.width = `${positive * 100}%`;
    document.querySelector("#negative-bar").style.width = `${negative * 100}%`;
  });
}

async function analyzeReview() {
  const text = reviewText.value.trim();
  if (!text) {
    setMessage("Please enter a hotel review before analyzing.", "error");
    reviewText.focus();
    return;
  }

  setLoading(true);
  setMessage("Analyzing the review with the BERT classifier...");

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Prediction could not be completed. Please try again.");
    }

    showResult(payload);
    setMessage("Prediction completed.");
  } catch (error) {
    setMessage(error.message || "Prediction could not be completed. Please try again.", "error");
  } finally {
    setLoading(false);
  }
}

reviewText.addEventListener("input", updateCharacterCount);
analyzeButton.addEventListener("click", analyzeReview);
clearButton.addEventListener("click", () => {
  reviewText.value = "";
  updateCharacterCount();
  setMessage();
  reviewText.focus();
});

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    reviewText.value = examples[button.dataset.example];
    updateCharacterCount();
    setMessage();
    reviewText.focus();
  });
});

updateCharacterCount();
