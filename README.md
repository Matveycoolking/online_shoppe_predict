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

Команда обучает Logistic Regression, Random Forest, CatBoost и дополнительно подбирает гиперпараметры для `Random Forest Tuned`. Если CatBoost недоступен, используется `HistGradientBoostingClassifier`.

Результаты сохраняются в:

- `models/best_model.pkl`
- `models/metadata.json`

## Результаты моделей

| Модель | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Random Forest Tuned | 0.8929 | 0.6482 | 0.6754 | 0.6615 | 0.9232 |
| CatBoost | 0.9019 | 0.7273 | 0.5864 | 0.6493 | 0.9295 |
| Logistic Regression | 0.8589 | 0.5291 | 0.8089 | 0.6398 | 0.9203 |
| Random Forest | 0.8978 | 0.7305 | 0.5393 | 0.6205 | 0.9202 |

Лучшая модель по F1-score — `Random Forest Tuned`.

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

## Docker

Docker запускает сразу два сервиса: FastAPI backend и статический frontend на nginx.

Сборка и запуск проекта:

```bash
docker compose up --build
```

После запуска доступны:

```text
Frontend: http://127.0.0.1:8080
Backend health: http://127.0.0.1:8000/health
Backend docs: http://127.0.0.1:8000/docs
```

Остановка контейнеров:

```bash
docker compose down
```

Быстрый запуск на Windows:

```text
run_project.bat
```

Этот файл запускает Docker Compose, ждёт готовности backend/frontend и открывает сайт в браузере. Для остановки можно использовать:

```text
stop_project.bat
```
