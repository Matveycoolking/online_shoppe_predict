const API_URL = "http://127.0.0.1:8000/predict";

const integerFields = [
  "Administrative",
  "Informational",
  "ProductRelated",
  "OperatingSystems",
  "Browser",
  "Region",
  "TrafficType",
];

const numericFields = [
  "Administrative_Duration",
  "Informational_Duration",
  "ProductRelated_Duration",
  "BounceRates",
  "ExitRates",
  "PageValues",
  "SpecialDay",
];

const form = document.querySelector("#prediction-form");
const button = document.querySelector("#submit-button");
const result = document.querySelector("#result");
const resultTitle = document.querySelector("#result-title");
const resultProbability = document.querySelector("#result-probability");

function buildPayload(formData) {
  const payload = {};

  integerFields.forEach((field) => {
    payload[field] = Number.parseInt(formData.get(field), 10);
  });

  numericFields.forEach((field) => {
    payload[field] = Number.parseFloat(formData.get(field));
  });

  payload.Month = formData.get("Month");
  payload.VisitorType = formData.get("VisitorType");
  payload.Weekend = formData.get("Weekend") === "true";

  return payload;
}

function showResult(data) {
  const probability = Math.round(data.purchase_probability * 100);
  result.className = `result-panel ${data.prediction ? "positive" : "negative"}`;
  resultTitle.textContent = data.prediction ? "Покупка вероятна" : "Покупка маловероятна";
  resultProbability.textContent = `Вероятность покупки: ${probability}%`;
}

function showError() {
  result.className = "result-panel error";
  resultTitle.textContent = "Не удалось получить прогноз";
  resultProbability.textContent = "Проверьте, запущен ли backend.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  button.textContent = "Запрос выполняется...";

  try {
    const payload = buildPayload(new FormData(form));
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    showResult(data);
  } catch (error) {
    showError();
  } finally {
    button.disabled = false;
    button.textContent = "Предсказать";
  }
});
