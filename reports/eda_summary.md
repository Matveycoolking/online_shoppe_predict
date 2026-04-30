# EDA Summary

## Размер датасета

- Строк: 12330
- Столбцов: 18

## Список колонок

- `Administrative`
- `Administrative_Duration`
- `Informational`
- `Informational_Duration`
- `ProductRelated`
- `ProductRelated_Duration`
- `BounceRates`
- `ExitRates`
- `PageValues`
- `SpecialDay`
- `Month`
- `OperatingSystems`
- `Browser`
- `Region`
- `TrafficType`
- `VisitorType`
- `Weekend`
- `Revenue`

## Типы данных

| column | dtype |
| --- | --- |
| Administrative | int64 |
| Administrative_Duration | float64 |
| Informational | int64 |
| Informational_Duration | float64 |
| ProductRelated | int64 |
| ProductRelated_Duration | float64 |
| BounceRates | float64 |
| ExitRates | float64 |
| PageValues | float64 |
| SpecialDay | float64 |
| Month | str |
| OperatingSystems | int64 |
| Browser | int64 |
| Region | int64 |
| TrafficType | int64 |
| VisitorType | str |
| Weekend | bool |
| Revenue | bool |

## Пропуски

| column | missing_count | missing_share |
| --- | --- | --- |
| Administrative | 0 | 0.0 |
| Administrative_Duration | 0 | 0.0 |
| Informational | 0 | 0.0 |
| Informational_Duration | 0 | 0.0 |
| ProductRelated | 0 | 0.0 |
| ProductRelated_Duration | 0 | 0.0 |
| BounceRates | 0 | 0.0 |
| ExitRates | 0 | 0.0 |
| PageValues | 0 | 0.0 |
| SpecialDay | 0 | 0.0 |
| Month | 0 | 0.0 |
| OperatingSystems | 0 | 0.0 |
| Browser | 0 | 0.0 |
| Region | 0 | 0.0 |
| TrafficType | 0 | 0.0 |
| VisitorType | 0 | 0.0 |
| Weekend | 0 | 0.0 |
| Revenue | 0 | 0.0 |

## Распределение целевой переменной

| Revenue | count |
| --- | --- |
| False | 10422 |
| True | 1908 |

Доля покупок: 15.47%.

Целевая переменная несбалансирована: покупок значительно меньше, чем сессий без покупки. Поэтому при оценке моделей необходимо использовать не только accuracy, но и precision, recall, F1-score и ROC-AUC.

## Описательная статистика числовых признаков

| column | count | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Administrative | 12330.0 | 2.3152 | 3.3218 | 0.0 | 0.0 | 1.0 | 4.0 | 27.0 |
| Administrative_Duration | 12330.0 | 80.8186 | 176.7791 | 0.0 | 0.0 | 7.5 | 93.2562 | 3398.75 |
| Informational | 12330.0 | 0.5036 | 1.2702 | 0.0 | 0.0 | 0.0 | 0.0 | 24.0 |
| Informational_Duration | 12330.0 | 34.4724 | 140.7493 | 0.0 | 0.0 | 0.0 | 0.0 | 2549.375 |
| ProductRelated | 12330.0 | 31.7315 | 44.4755 | 0.0 | 7.0 | 18.0 | 38.0 | 705.0 |
| ProductRelated_Duration | 12330.0 | 1194.7462 | 1913.6693 | 0.0 | 184.1375 | 598.9369 | 1464.1572 | 63973.5222 |
| BounceRates | 12330.0 | 0.0222 | 0.0485 | 0.0 | 0.0 | 0.0031 | 0.0168 | 0.2 |
| ExitRates | 12330.0 | 0.0431 | 0.0486 | 0.0 | 0.0143 | 0.0252 | 0.05 | 0.2 |
| PageValues | 12330.0 | 5.8893 | 18.5684 | 0.0 | 0.0 | 0.0 | 0.0 | 361.7637 |
| SpecialDay | 12330.0 | 0.0614 | 0.1989 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |

## Краткие выводы

- В датасете нет критических проблем со структурой: ожидаемые колонки присутствуют.
- Покупки составляют меньшую часть наблюдений, поэтому задача чувствительна к дисбалансу классов.
- Поведенческие признаки вроде `PageValues`, `ExitRates` и `BounceRates` важны для дальнейшего анализа.
- Выбросы в поведенческих признаках могут отражать реальные сессии пользователей, поэтому они не удалялись автоматически.

## Сохранённые графики

- `reports/figures/target_distribution.png`
- `reports/figures/correlation_matrix.png`
- `reports/figures/revenue_by_month.png`
- `reports/figures/revenue_by_visitor_type.png`
- `reports/figures/revenue_by_weekend.png`
- `reports/figures/pagevalues_distribution.png`
- `reports/figures/exitrates_distribution.png`
- `reports/figures/bouncerates_distribution.png`
- `reports/figures/numeric_boxplots.png`
