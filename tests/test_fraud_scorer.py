from dataclasses import replace
from decimal import Decimal
import pytest
from app.domain.fraud_scorer import FraudScorer
from app.domain.transaction import FraudDecision, Transaction, TransactionChannel

@pytest.fixture
def scorer():
    return FraudScorer()

@pytest.fixture
def safe_transaction():
    return Transaction(
        amount=Decimal("25.00"), currency="GBP", merchant_category_code="5411",
        channel=TransactionChannel.CONTACTLESS, country_code="GB",
        card_holder_country="GB", hour_of_day=14, is_international=False,
    )

def test_safe_transaction_scores_low(scorer, safe_transaction):
    result = scorer.score(safe_transaction)
    assert result.score < 0.4
    assert result.decision == FraudDecision.ALLOW

def test_high_amount_raises_score(scorer, safe_transaction):
    big_txn = replace(safe_transaction, amount=Decimal("3000.00"))
    result = scorer.score(big_txn)
    assert result.score >= 0.3
    assert any("High amount" in r for r in result.top_reasons)

def test_late_night_international_blocked(scorer, safe_transaction):
    risky_txn = replace(safe_transaction, hour_of_day=3, is_international=True, country_code="RO")
    result = scorer.score(risky_txn)
    assert result.decision == FraudDecision.BLOCK
    assert result.score >= 0.7

def test_score_never_exceeds_one(scorer, safe_transaction):
    worst_case = replace(
        safe_transaction, amount=Decimal("9999.99"), hour_of_day=3,
        is_international=True, country_code="NG",
    )
    result = scorer.score(worst_case)
    assert 0.0 <= result.score <= 1.0
