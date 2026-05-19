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

const samples = {
  low: {
    Administrative: 0,
    Administrative_Duration: 0,
    Informational: 0,
    Informational_Duration: 0,
    ProductRelated: 4,
    ProductRelated_Duration: 85,
    BounceRates: 0.08,
    ExitRates: 0.12,
    PageValues: 0,
    SpecialDay: 0,
    Month: "May",
    OperatingSystems: 2,
    Browser: 2,
    Region: 1,
    TrafficType: 3,
    VisitorType: "Returning_Visitor",
    Weekend: false,
  },
  high: {
    Administrative: 4,
    Administrative_Duration: 120,
    Informational: 1,
    Informational_Duration: 35,
    ProductRelated: 38,
    ProductRelated_Duration: 1850,
    BounceRates: 0.005,
    ExitRates: 0.018,
    PageValues: 32,
    SpecialDay: 0,
    Month: "Nov",
    OperatingSystems: 2,
    Browser: 2,
    Region: 1,
    TrafficType: 2,
    VisitorType: "New_Visitor",
    Weekend: true,
  },
};

const form = document.querySelector("#prediction-form");
const button = document.querySelector("#submit-button");
const result = document.querySelector("#result");
const resultTitle = document.querySelector("#result-title");
const resultProbability = document.querySelector("#result-probability");
const probabilityFill = document.querySelector("#probability-fill");
const scoreValue = document.querySelector("#score-value");

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

function setProbabilityMeter(probability) {
  const percent = Math.max(0, Math.min(100, Math.round(probability * 100)));
  probabilityFill.style.width = `${percent}%`;
  result.style.setProperty("--score", `${percent}%`);
  scoreValue.textContent = `${percent}%`;
  return percent;
}

function showResult(data) {
  const probability = setProbabilityMeter(data.purchase_probability);
  result.className = `result-panel has-result ${data.prediction ? "positive" : "negative"}`;
  resultTitle.textContent = data.prediction ? "Покупка вероятна" : "Покупка маловероятна";
  resultProbability.textContent = `Вероятность покупки: ${probability}%`;
}

function showError() {
  result.className = "result-panel has-result error";
  resultTitle.textContent = "Не удалось получить прогноз";
  resultProbability.textContent = "Проверьте, что backend запущен и доступен на порту 8000.";
  setProbabilityMeter(0);
}

function fillSample(sampleName) {
  const sample = samples[sampleName];
  if (!sample) {
    return;
  }

  Object.entries(sample).forEach(([field, value]) => {
    const control = form.elements[field];
    if (!control) {
      return;
    }
    control.value = String(value);
  });
}

document.querySelectorAll("[data-sample]").forEach((sampleButton) => {
  sampleButton.addEventListener("click", () => {
    fillSample(sampleButton.dataset.sample);
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  button.textContent = "Выполняю прогноз...";

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
    button.textContent = "Получить прогноз";
  }
});
