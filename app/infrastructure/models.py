"""ORM models — describe database rows, kept separate from domain models."""
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import Numeric, String, DateTime, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.infrastructure.database import Base

class TransactionRecord(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3))
    merchant_category_code: Mapped[str] = mapped_column(String(4))
    channel: Mapped[str] = mapped_column(String(20))
    country_code: Mapped[str] = mapped_column(String(2))
    card_holder_country: Mapped[str] = mapped_column(String(2))
    hour_of_day: Mapped[int]
    is_international: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    fraud_score: Mapped[float] = mapped_column(Float)
    fraud_decision: Mapped[str] = mapped_column(String(10))
    top_reasons: Mapped[list] = mapped_column(JSON)
    model_version: Mapped[str] = mapped_column(String(50))
