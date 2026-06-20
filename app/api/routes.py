from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_fraud_scorer
from app.domain.fraud_scorer import FraudScorer
from app.domain.transaction import Transaction, TransactionChannel
from app.infrastructure.database import get_db
from app.infrastructure.models import TransactionRecord
from app.schemas.transaction import FraudScoreResponse, TransactionCreate

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=FraudScoreResponse, status_code=status.HTTP_201_CREATED)
async def score_transaction(
    payload: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    scorer: FraudScorer = Depends(get_fraud_scorer),
) -> FraudScoreResponse:
    try:
        channel = TransactionChannel(payload.channel)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid channel: {payload.channel}. "
                   f"Must be one of: {[c.value for c in TransactionChannel]}",
        )

    txn = Transaction(
        amount=payload.amount, currency=payload.currency,
        merchant_category_code=payload.merchant_category_code, channel=channel,
        country_code=payload.country_code, card_holder_country=payload.card_holder_country,
        hour_of_day=payload.hour_of_day, is_international=payload.is_international,
    )

    fraud_score = scorer.score(txn)

    record = TransactionRecord(
        id=txn.transaction_id, amount=txn.amount, currency=txn.currency,
        merchant_category_code=txn.merchant_category_code, channel=txn.channel.value,
        country_code=txn.country_code, card_holder_country=txn.card_holder_country,
        hour_of_day=txn.hour_of_day, is_international=txn.is_international,
        created_at=txn.created_at, fraud_score=fraud_score.score,
        fraud_decision=fraud_score.decision.value, top_reasons=fraud_score.top_reasons,
        model_version=fraud_score.model_version,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    return FraudScoreResponse.model_validate({
        "transaction_id": record.id,
        "score": record.fraud_score,
        "decision": record.fraud_decision,
        "top_reasons": record.top_reasons,
        "model_version": record.model_version,
        "created_at": record.created_at,
    })

@router.get("/{transaction_id}", response_model=FraudScoreResponse)
async def get_transaction(transaction_id: str, db: AsyncSession = Depends(get_db)) -> FraudScoreResponse:
    result = await db.execute(select(TransactionRecord).where(TransactionRecord.id == transaction_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return FraudScoreResponse.model_validate({
        "transaction_id": record.id,
        "score": record.fraud_score,
        "decision": record.fraud_decision,
        "top_reasons": record.top_reasons,
        "model_version": record.model_version,
        "created_at": record.created_at,
    })
