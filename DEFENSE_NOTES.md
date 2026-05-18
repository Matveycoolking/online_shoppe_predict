# Как защищать проект

1. Постановка задачи: нужно предсказать, завершится ли сессия интернет-магазина покупкой.
2. Тип задачи: бинарная классификация, целевая переменная `Revenue`.
3. Данные: Online Shoppers Purchasing Intention Dataset, 12330 строк и 18 исходных колонок.
4. Дисбаланс классов: покупок около 15.47%, поэтому одной accuracy недостаточно.
5. Feature engineering: добавлены `TotalPages`, `TotalDuration`, `ProductPagesShare`, `AvgProductDuration`, `HasPageValue`.
6. Предобработка: числовые признаки проходят imputer и scaling, категориальные признаки проходят imputer и OneHotEncoder.
7. Модели: Logistic Regression, Random Forest, CatBoost и Random Forest Tuned.
8. Сравнение: используются Accuracy, Precision, Recall, F1-score, ROC-AUC и Confusion Matrix.
9. Лучшая модель: Random Forest Tuned выбран по F1-score, так как лучше балансирует precision и recall.
10. Backend: FastAPI endpoint `/predict` принимает сырые признаки и возвращает прогноз.
11. Frontend: HTML/CSS/JavaScript форма отправляет признаки в backend и показывает вероятность покупки.
