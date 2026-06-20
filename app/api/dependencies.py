"""Shared FastAPI dependencies."""
from app.domain.fraud_scorer import FraudScorer

_scorer = FraudScorer()

def get_fraud_scorer() -> FraudScorer:
    return _scorer
