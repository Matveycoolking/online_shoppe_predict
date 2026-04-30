# Как защищать проект

1. Постановка задачи: нужно предсказать, завершится ли сессия интернет-магазина покупкой.
2. Тип задачи: бинарная классификация, целевая переменная `Revenue`.
3. Данные: UCI Online Shoppers Purchasing Intention Dataset, 12330 строк и 18 колонок.
4. Дисбаланс классов: покупок около 15.47%, поэтому accuracy недостаточно.
5. Предобработка: числовые признаки проходят imputer и scaling, категориальные признаки проходят imputer и OneHotEncoder.
6. Модели: Logistic Regression, Random Forest, CatBoost.
7. Сравнение: используются Accuracy, Precision, Recall, F1-score, ROC-AUC и Confusion Matrix.
8. Лучшая модель: CatBoost выбран по F1-score и дополнительно имеет высокий ROC-AUC.
9. Backend: FastAPI endpoint `/predict` принимает сырые признаки и возвращает прогноз.
10. Frontend: HTML/CSS/JavaScript форма отправляет признаки в backend и показывает вероятность покупки.
