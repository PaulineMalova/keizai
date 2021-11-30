import uuid

from sqlalchemy import Column, ForeignKey, Float, String, Enum
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from app.base.model import Base
from app.enums import TransactionTypeEnum, SourceAccountEnum


class Account(Base):

    __tablename__ = "account"

    account_id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = Column(
        UUIDType(binary=False), ForeignKey("user.user_id"), nullable=False
    )
    account_balance = Column(Float, nullable=False, default=0)
    account_savings = Column(Float, nullable=False, default=0)
    # cash_balance = Column(Float, nullable=False, default=0)

    def __repr__(self):
        return str(self.account_id)


class AccountTransactionCategory(Base):
    """Used to track the transaction categories for a given account"""

    __tablename__ = "account_transaction_category"

    account_transaction_category_id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    account_id = Column(
        UUIDType(binary=False),
        ForeignKey("account.account_id"),
        nullable=False,
    )
    category_name = Column(String, nullable=False)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)

    def __repr__(self):
        return str(self.account_transaction_category_id)


class Ledger(Base):

    """Used to track the transactions made in an account"""

    __tablename__ = "ledger"

    ledger_id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    account_id = Column(
        UUIDType(binary=False),
        ForeignKey("account.account_id"),
        nullable=False,
    )
    transaction_category_id = Column(
        UUIDType(binary=False),
        ForeignKey(
            "account_transaction_category.account_transaction_category_id"
        ),
        nullable=False,
    )
    amount = Column(Float, nullable=False)
    transaction_cost = Column(Float, nullable=False)
    source_account = Column(Enum(SourceAccountEnum), nullable=False)
    account = relationship("Account", lazy="joined")
    transaction_category = relationship("AccountTransactionCategory")

    def __repr__(self):
        return str(self.ledger_id)
