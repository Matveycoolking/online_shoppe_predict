# Покупательское намерение в интернет-магазине

ML-сервис для прогнозирования вероятности покупки по параметрам пользовательской сессии интернет-магазина.

Проект решает задачу бинарной классификации:

- `Revenue = 0` — покупка не совершена;
- `Revenue = 1` — покупка совершена.

## Запуск проекта

Команды выполняются из корня проекта:

```powershell
cd C:\Users\где находиться проект
```

### 1. Консольный запуск

Установить зависимости:

```powershell
python -m pip install -r requirements.txt
```

Проверить загрузку данных:

```powershell
python -c "from src.data_loading import load_data; df = load_data(); print(df.shape)"
```

При необходимости переобучить модель:

```powershell
python -m src.train
```

Запустить backend:

```powershell
python -m uvicorn backend.main:app --reload
```

Открыть frontend:

```powershell
Start-Process .\frontend\index.html
```

Адреса после запуска backend:

```text
API docs: http://127.0.0.1:8000/docs
Health:   http://127.0.0.1:8000/health
Predict:  http://127.0.0.1:8000/predict
```

### 2. Быстрый запуск

Через Docker Compose:

```powershell
docker compose up --build
```

После запуска:

```text
Frontend:     http://127.0.0.1:8080
Backend docs: http://127.0.0.1:8000/docs
```

Остановка:

```powershell
docker compose down
```

Быстрый запуск на Windows через bat-файл:

```powershell
.\run_project.bat
```

Остановка на Windows:

```powershell
.\stop_project.bat
```

## Данные

Используется датасет **UCI Online Shoppers Purchasing Intention Dataset**.

Файл с данными:

```text
data/data.csv
```

Основные признаки:

- поведение на сайте: `Administrative`, `Informational`, `ProductRelated` и длительности;
- качество сессии: `BounceRates`, `ExitRates`, `PageValues`, `SpecialDay`;
- контекст визита: `Month`, `VisitorType`, `Weekend`;
- технические признаки: `OperatingSystems`, `Browser`, `Region`, `TrafficType`;
- целевая переменная: `Revenue`.

В данных есть дисбаланс классов: покупок заметно меньше, чем сессий без покупки. Поэтому для оценки используются не только `accuracy`, но и `precision`, `recall`, `F1-score`, `ROC-AUC`, `PR-AUC`, `balanced_accuracy`.

## Структура проекта

```text
backend/       FastAPI backend
data/          датасет
doc/           презентация и материалы защиты
frontend/      статический frontend
GoogleColab/   notebooks с EDA и обучением
models/        сохранённая модель и metadata
src/           код загрузки данных, preprocessing, обучения и предсказания
```

Ключевые файлы:

```text
src/train.py          обучение и сравнение моделей
src/predict.py        загрузка модели и single prediction
src/preprocessing.py  feature engineering и preprocessing pipeline
backend/main.py       API сервиса
frontend/index.html   интерфейс для демонстрации
docker-compose.yml    запуск backend и frontend
```

## Обучение модели

```bash
python -m src.train
```

Обучаются и сравниваются:

- Logistic Regression;
- Random Forest;
- CatBoost;
- Random Forest Tuned.

Лучший pipeline сохраняется в:

```text
models/best_model.pkl
models/metadata.json
```

## Результаты

Финальная модель: **Random Forest Tuned**.

Метрики на test-выборке:

| Метрика | Значение |
|---|---:|
| Accuracy | 0.8978 |
| Balanced accuracy | 0.8081 |
| Precision | 0.6675 |
| Recall | 0.6780 |
| F1-score | 0.6727 |
| ROC-AUC | 0.9253 |
| PR-AUC | 0.7347 |

Для анализа дисбаланса и переобучения дополнительно проверялись:

- регуляризация Random Forest;
- resampling: RandomOverSampler, SMOTE, RandomUnderSampler;
- подбор threshold;
- cross-validation.

Итоговая модель оставлена по лучшему `F1-score` на test-выборке.

## Single prediction

```bash
python -c "from src.predict import predict_single; print(predict_single({'Administrative': 1, 'Administrative_Duration': 20.5, 'Informational': 0, 'Informational_Duration': 0.0, 'ProductRelated': 5, 'ProductRelated_Duration': 120.0, 'BounceRates': 0.02, 'ExitRates': 0.05, 'PageValues': 10.0, 'SpecialDay': 0.0, 'Month': 'Nov', 'OperatingSystems': 2, 'Browser': 2, 'Region': 1, 'TrafficType': 3, 'VisitorType': 'Returning_Visitor', 'Weekend': False}))"
```

## API

Пример запроса:

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

## Frontend

Frontend находится в папке:

```text
frontend/
```

Форма отправляет запрос в backend и показывает:

- прогноз класса;
- вероятность покупки;
- визуальный индикатор вероятности.
