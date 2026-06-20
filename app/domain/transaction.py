"""Domain models — pure business concepts, zero framework dependencies."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

class TransactionChannel(str, Enum):
    ONLINE = "online"
    CONTACTLESS = "contactless"
    ATM = "atm"
    CHIP_AND_PIN = "chip_and_pin"

class FraudDecision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"

@dataclass
class Transaction:
    amount: Decimal
    currency: str
    merchant_category_code: str
    channel: TransactionChannel
    country_code: str
    card_holder_country: str
    hour_of_day: int
    is_international: bool
    transaction_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class FraudScore:
    transaction_id: UUID
    score: float
    decision: FraudDecision
    top_reasons: list[str]
    model_version: str
