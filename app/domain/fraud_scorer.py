"""Service class containing business logic. No HTTP, no database."""
from decimal import Decimal
from app.domain.transaction import FraudDecision, FraudScore, Transaction

HIGH_AMOUNT_THRESHOLD = Decimal("2000.00")
SUSPICIOUS_HOUR_START = 1
SUSPICIOUS_HOUR_END = 4
HIGH_RISK_COUNTRIES = {"NG", "RO", "UA", "VN"}
MODEL_VERSION = "rules-baseline-v1"

class FraudScorer:
    def score(self, txn: Transaction) -> FraudScore:
        risk_signals: list[str] = []
        raw_score = 0.0

        if txn.amount > HIGH_AMOUNT_THRESHOLD:
            raw_score += 0.3
            risk_signals.append(f"High amount: {txn.amount} {txn.currency}")

        if txn.is_international:
            raw_score += 0.2
            risk_signals.append("International transaction")

        if SUSPICIOUS_HOUR_START <= txn.hour_of_day <= SUSPICIOUS_HOUR_END:
            raw_score += 0.25
            risk_signals.append(f"Unusual hour: {txn.hour_of_day:02d}:00")

        if txn.country_code in HIGH_RISK_COUNTRIES:
            raw_score += 0.25
            risk_signals.append(f"High-risk country: {txn.country_code}")

        raw_score = min(raw_score, 1.0)
        decision = self._decide(raw_score)

        return FraudScore(
            transaction_id=txn.transaction_id,
            score=round(raw_score, 4),
            decision=decision,
            top_reasons=risk_signals[:3],
            model_version=MODEL_VERSION,
        )

    def _decide(self, score: float) -> FraudDecision:
        if score >= 0.7:
            return FraudDecision.BLOCK
        if score >= 0.4:
            return FraudDecision.REVIEW
        return FraudDecision.ALLOW
