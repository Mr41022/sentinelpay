"""Pydantic schemas — what crosses the HTTP boundary, validated."""
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

class TransactionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    merchant_category_code: str = Field(..., min_length=4, max_length=4)
    channel: str
    country_code: str = Field(..., min_length=2, max_length=2)
    card_holder_country: str = Field(..., min_length=2, max_length=2)
    hour_of_day: int = Field(..., ge=0, le=23)
    is_international: bool

    @field_validator("currency", "country_code", "card_holder_country")
    @classmethod
    def uppercase_codes(cls, v: str) -> str:
        return v.upper()

    model_config = {
        "json_schema_extra": {
            "example": {
                "amount": "150.00", "currency": "GBP",
                "merchant_category_code": "5411", "channel": "contactless",
                "country_code": "GB", "card_holder_country": "GB",
                "hour_of_day": 14, "is_international": False,
            }
        }
    }

class FraudScoreResponse(BaseModel):
    transaction_id: UUID
    score: float
    decision: str
    top_reasons: list[str]
    model_version: str
    created_at: datetime
    model_config = {"from_attributes": True}
