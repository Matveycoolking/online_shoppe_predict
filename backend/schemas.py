"""Pydantic schemas for the prediction API."""

from pydantic import BaseModel


class ShopperSession(BaseModel):
    """Raw shopper session features accepted by the API."""

    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: str
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: str
    Weekend: bool


class PredictionResponse(BaseModel):
    """Prediction response returned by the API."""

    prediction: bool
    prediction_label: str
    purchase_probability: float
