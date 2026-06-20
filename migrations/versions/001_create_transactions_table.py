"""create transactions table

Revision ID: 001
Revises: 
Create Date: 2026-06-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('merchant_category_code', sa.String(length=4), nullable=False),
        sa.Column('channel', sa.String(length=20), nullable=False),
        sa.Column('country_code', sa.String(length=2), nullable=False),
        sa.Column('card_holder_country', sa.String(length=2), nullable=False),
        sa.Column('hour_of_day', sa.Integer(), nullable=False),
        sa.Column('is_international', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('fraud_score', sa.Float(), nullable=False),
        sa.Column('fraud_decision', sa.String(length=10), nullable=False),
        sa.Column('top_reasons', sa.JSON(), nullable=False),
        sa.Column('model_version', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('transactions')
