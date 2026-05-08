# Покупательское намерение в интернет-магазине

Учебный итоговый ML-проект: система прогнозирует, завершится ли пользовательская сессия интернет-магазина покупкой.

## Задача

Это задача бинарной классификации. Целевая переменная:

```text
Revenue
```

- `False` / `0` — покупка не совершена.
- `True` / `1` — покупка совершена.

## Датасет

Используется UCI Online Shoppers Purchasing Intention Dataset. Файл с данными должен находиться в `data/data.csv`.

Признаки:

- `Administrative`, `Administrative_Duration`
- `Informational`, `Informational_Duration`
- `ProductRelated`, `ProductRelated_Duration`
- `BounceRates`, `ExitRates`, `PageValues`, `SpecialDay`
- `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`, `VisitorType`, `Weekend`
- `Revenue`

## Структура проекта

```text
data/
notebooks/
reports/
reports/figures/
models/
src/
backend/
frontend/
AGENTS.md
sprints.md
README.md
REPORT.md
DEFENSE_NOTES.md
requirements.txt
```

## Установка

Команды нужно запускать из корня проекта:

```bash
cd C:\Users\matve\Desktop\InternetBying
python -m pip install -r requirements.txt
```

## Проверка загрузки данных

```bash
python -c "from src.data_loading import load_data; df = load_data(); print(df.shape); print(df.head())"
```

## EDA

```bash
python -m src.eda
```

Графики сохраняются в `reports/figures/`, текстовый отчёт — в `reports/eda_summary.md`.

## Google Colab

Для защиты анализ, обучение и сравнение моделей также перенесены в самостоятельный notebook:

```text
notebooks/online_shopper_intention_colab.ipynb
```

Как использовать:

1. Открыть notebook в Google Colab.
2. Запустить ячейки сверху вниз.
3. В ячейке загрузки выбрать файл `data.csv`.
4. После обучения скачать `best_model.pkl`, `metadata.json` и `model_comparison.csv`.
5. При необходимости положить скачанные файлы в локальный проект:
   - `models/best_model.pkl`
   - `models/metadata.json`
   - `reports/model_comparison.csv`

## Обучение моделей

```bash
python -m src.train
```

Команда обучает Logistic Regression, Random Forest и CatBoost. Если CatBoost недоступен, используется `HistGradientBoostingClassifier`.

Результаты сохраняются в:

- `reports/model_comparison.csv`
- `models/best_model.pkl`
- `models/metadata.json`

## Результаты моделей

| Модель | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| CatBoost | 0.8998 | 0.7170 | 0.5838 | 0.6436 | 0.9272 |
| Logistic Regression | 0.8410 | 0.4913 | 0.7435 | 0.5917 | 0.8932 |
| Random Forest | 0.8942 | 0.7619 | 0.4607 | 0.5742 | 0.9182 |

Лучшая модель по F1-score — `CatBoost`.

## Проверка single prediction

```bash
python -c "from src.predict import predict_single; print(predict_single({'Administrative': 1, 'Administrative_Duration': 20.5, 'Informational': 0, 'Informational_Duration': 0.0, 'ProductRelated': 5, 'ProductRelated_Duration': 120.0, 'BounceRates': 0.02, 'ExitRates': 0.05, 'PageValues': 10.0, 'SpecialDay': 0.0, 'Month': 'Nov', 'OperatingSystems': 2, 'Browser': 2, 'Region': 1, 'TrafficType': 3, 'VisitorType': 'Returning_Visitor', 'Weekend': False}))"
```

## Запуск backend

```bash
python -m uvicorn backend.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

## Пример API-запроса

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "Administrative": 1,
  "Administrative_Duration": 20.5,
  "Informational": 0,
  "Informational_Duration": 0.0,
  "ProductRelated": 5,
  "ProductRelated_Duration": 120.0,
  "BounceRates": 0.02,
  "ExitRates": 0.05,
  "PageValues": 10.0,
  "SpecialDay": 0.0,
  "Month": "Nov",
  "OperatingSystems": 2,
  "Browser": 2,
  "Region": 1,
  "TrafficType": 3,
  "VisitorType": "Returning_Visitor",
  "Weekend": false
}'
```

## Запуск frontend

1. Обучить модель:

```bash
python -m src.train
```

2. Запустить backend:

```bash
python -m uvicorn backend.main:app --reload
```

3. Открыть файл:

```text
frontend/index.html
```

Форма отправляет запрос на `http://127.0.0.1:8000/predict` и показывает прогноз вместе с вероятностью покупки.

## Защита проекта

Краткий сценарий защиты находится в `DEFENSE_NOTES.md`.
