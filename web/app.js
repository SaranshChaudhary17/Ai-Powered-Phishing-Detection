// When deploying to GitHub Pages, change this to your Hugging Face Space URL.
// Example: const API_BASE_URL = "https://yourusername-yourspacename.hf.space";
const API_BASE_URL = "https://saranshchaudhary17-phishing-detector.hf.space";

const form = document.getElementById("scan-form");
const urlInput = document.getElementById("url-input");
const thresholdInput = document.getElementById("threshold-input");
const thresholdValue = document.getElementById("threshold-value");
const statusText = document.getElementById("status-text");
const resultEmpty = document.getElementById("result-empty");
const resultPanel = document.getElementById("result-panel");
const resultLabel = document.getElementById("result-label");
const resultPill = document.getElementById("result-pill");
const riskValue = document.getElementById("risk-value");
const confidenceValue = document.getElementById("confidence-value");
const thresholdDisplay = document.getElementById("threshold-display");
const resultSummary = document.getElementById("result-summary");
const featureGrid = document.getElementById("feature-grid");
const exampleBtn = document.getElementById("example-btn");
const riskBar = document.getElementById("risk-bar");

thresholdInput.addEventListener("input", () => {
  thresholdValue.textContent = Number(thresholdInput.value).toFixed(2);
});

exampleBtn.addEventListener("click", async () => {
  statusText.textContent = "Loading example URL...";
  const response = await fetch(`${API_BASE_URL}/api/example`);
  const data = await response.json();
  urlInput.value = data.url;
  thresholdInput.value = data.threshold.toFixed(2);
  thresholdValue.textContent = data.threshold.toFixed(2);
  renderResult(data);
  statusText.textContent = "Example loaded.";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const url = urlInput.value.trim();
  if (!url) {
    statusText.textContent = "Please enter a URL first.";
    return;
  }

  const threshold = Number(thresholdInput.value);
  statusText.textContent = "Analyzing URL with your model...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url, threshold })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction failed.");
    }

    renderResult(data);
    statusText.textContent = "Analysis complete.";
  } catch (error) {
    statusText.textContent = error.message;
  }
});

function renderResult(data) {
  resultEmpty.classList.add("hidden");
  resultPanel.classList.remove("hidden");

  const safe = data.prediction === "good";
  resultLabel.textContent = safe ? "Good URL" : "Phishing Risk";
  resultLabel.className = safe ? "risk-safe" : "risk-danger";

  resultPill.textContent = safe ? "Likely Safe" : "High Risk";
  resultPill.className = `pill ${safe ? "pill-safe" : "pill-danger"}`;

  riskValue.textContent = `${data.risk_percent.toFixed(2)}%`;
  confidenceValue.textContent = `${data.confidence_percent.toFixed(2)}%`;
  thresholdDisplay.textContent = Number(data.threshold).toFixed(2);
  riskBar.style.width = `${Math.min(100, data.risk_percent)}%`;
  riskBar.style.background = safe
    ? "linear-gradient(90deg, #7ab08a, #3f7f57)"
    : "linear-gradient(90deg, #f1b55f, #c75b49)";

  resultSummary.textContent = safe
    ? "The model considers this URL closer to the benign pattern learned from your dataset."
    : "The model found a phishing-like pattern based on the feature signals extracted from the URL.";

  featureGrid.innerHTML = "";
  Object.entries(data.features).forEach(([key, value]) => {
    const item = document.createElement("div");
    item.className = "feature-item";
    item.innerHTML = `
      <span>${formatFeatureName(key)}</span>
      <strong>${formatFeatureValue(value)}</strong>
    `;
    featureGrid.appendChild(item);
  });
}

function formatFeatureName(name) {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatFeatureValue(value) {
  if (typeof value === "number") {
    return Number.isInteger(value) ? `${value}` : value.toFixed(4);
  }
  return String(value);
}
